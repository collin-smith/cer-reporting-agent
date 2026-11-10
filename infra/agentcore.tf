# Article 7's AgentCore window (D55): the reviewing agent and the MCP tools hosted on Bedrock AgentCore, for one
# measured run, then switched off the same day. Off by default; nothing here exists unless agentcore_window = true.
#
#   agent    AgentCore Runtime, HTTP: the same agent.run as every eval (cer_agent/runtime.py), Nova Lite through the
#            tagged profile, prompt caching on as in the gate
#   tools    AgentCore Runtime, MCP: the MCP server's public tools (triage_report, decide, rule_text, draft_notice)
#   gateway  AgentCore Gateway in front of `tools`, inbound auth AWS_IAM (SigV4 from the caller's credentials), and
#            the Gateway signs its own calls to the tools Runtime with its role
#
# Build the zip first:  .venv/bin/python scripts/build_agentcore.py   (writes infra/build/agentcore.zip)
# On:   terraform apply -var agentcore_window=true      Off:  terraform apply   (default false destroys it all)
#
# Cost (Price List, ca-central-1, 2026-11-10): Runtime $0.0895 per vCPU-hour while the CPU works (not while it waits
# on the model) and $0.00945 per GB-hour of memory for the session's life, so sessions end 60 s after going idle;
# Gateway $0.005 per 1,000 calls, $0.0002 per indexed tool a month; S3 for one ~30 MB zip. Nothing bills while idle.

variable "agentcore_window" {
  description = "Article 7's AgentCore window (D55): true deploys the agent and tools Runtimes and the Gateway."
  type        = bool
  default     = false
}

locals {
  ac            = var.agentcore_window ? 1 : 0
  agentcore_zip = "${path.module}/build/agentcore.zip"
  ac_name       = replace(local.name, "-", "_") # Runtime names allow letters, digits and underscores only
}

# --- The code: one zip, two entry files ---

resource "aws_s3_bucket" "agentcore_code" {
  count         = local.ac
  bucket        = "${local.name}-agentcore-code-${local.account_id}"
  force_destroy = true # the window's teardown removes the zip with the bucket
}

resource "aws_s3_bucket_public_access_block" "agentcore_code" {
  count                   = local.ac
  bucket                  = aws_s3_bucket.agentcore_code[0].id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_object" "agentcore_zip" {
  count  = local.ac
  bucket = aws_s3_bucket.agentcore_code[0].id
  key    = "agentcore-${filemd5(local.agentcore_zip)}.zip" # a new key per build, so the Runtimes pick it up
  source = local.agentcore_zip
  etag   = filemd5(local.agentcore_zip)
}

# --- Runtime execution role (both Runtimes) ---

resource "aws_iam_role" "agentcore_runtime" {
  count = local.ac
  name  = "${local.name}-agentcore-runtime"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "bedrock-agentcore.amazonaws.com" }
      Action    = "sts:AssumeRole"
      Condition = {
        StringEquals = { "aws:SourceAccount" = local.account_id }
        ArnLike      = { "aws:SourceArn" = "arn:aws:bedrock-agentcore:${var.region}:${local.account_id}:*" }
      }
    }]
  })
}

resource "aws_iam_role_policy" "agentcore_runtime" {
  count = local.ac
  role  = aws_iam_role.agentcore_runtime[0].id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "NovaLiteThroughTheTaggedProfile" # as the approval Lambda: no other model
        Effect = "Allow"
        Action = "bedrock:InvokeModel"
        Resource = [
          aws_bedrock_inference_profile.nova_lite.arn,
          "arn:aws:bedrock:*:${local.account_id}:inference-profile/ca.amazon.nova-lite-v1:0",
          "arn:aws:bedrock:*::foundation-model/amazon.nova-lite-v1:0",
        ]
      },
      {
        Sid      = "Code"
        Effect   = "Allow"
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.agentcore_code[0].arn}/*"
      },
      {
        Sid      = "LogGroups"
        Effect   = "Allow"
        Action   = ["logs:DescribeLogStreams", "logs:CreateLogGroup"]
        Resource = "arn:aws:logs:${var.region}:${local.account_id}:log-group:/aws/bedrock-agentcore/runtimes/*"
      },
      {
        Sid      = "DescribeLogGroups"
        Effect   = "Allow"
        Action   = "logs:DescribeLogGroups"
        Resource = "arn:aws:logs:${var.region}:${local.account_id}:log-group:*"
      },
      {
        Sid      = "LogEvents"
        Effect   = "Allow"
        Action   = ["logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "arn:aws:logs:${var.region}:${local.account_id}:log-group:/aws/bedrock-agentcore/runtimes/*:log-stream:*"
      },
      {
        Sid      = "Traces"
        Effect   = "Allow"
        Action   = ["xray:PutTraceSegments", "xray:PutTelemetryRecords", "xray:GetSamplingRules", "xray:GetSamplingTargets"]
        Resource = "*"
      },
      {
        Sid       = "Metrics"
        Effect    = "Allow"
        Action    = "cloudwatch:PutMetricData"
        Resource  = "*"
        Condition = { StringEquals = { "cloudwatch:namespace" = "bedrock-agentcore" } }
      },
      {
        Sid    = "WorkloadIdentity"
        Effect = "Allow"
        Action = ["bedrock-agentcore:GetWorkloadAccessToken", "bedrock-agentcore:GetWorkloadAccessTokenForJWT"]
        Resource = [
          "arn:aws:bedrock-agentcore:${var.region}:${local.account_id}:workload-identity-directory/default",
          "arn:aws:bedrock-agentcore:${var.region}:${local.account_id}:workload-identity-directory/default/workload-identity/${local.ac_name}_*",
        ]
      },
    ]
  })
}

# --- The two Runtimes ---

locals {
  runtime_env = {
    NOVA_LITE_ARN    = aws_bedrock_inference_profile.nova_lite.arn
    CER_PROMPT_CACHE = "1" # as in the deployed gate (D53)
  }
}

resource "aws_bedrockagentcore_agent_runtime" "agent" {
  count              = local.ac
  agent_runtime_name = "${local.ac_name}_agent"
  description        = "The reviewing agent (article 7, D55): Nova Lite reads, the rules engine decides."
  role_arn           = aws_iam_role.agentcore_runtime[0].arn

  agent_runtime_artifact {
    code_configuration {
      entry_point = ["agent_main.py"]
      runtime     = "PYTHON_3_14"
      code {
        s3 {
          bucket = aws_s3_bucket.agentcore_code[0].id
          prefix = aws_s3_object.agentcore_zip[0].key
        }
      }
    }
  }

  network_configuration {
    network_mode = "PUBLIC"
  }
  protocol_configuration {
    server_protocol = "HTTP"
  }
  lifecycle_configuration {
    idle_runtime_session_timeout = 60  # memory bills until the session ends: end it a minute after the reply
    max_lifetime                 = 900 # no session outlives 15 minutes
  }
  environment_variables = local.runtime_env

  depends_on = [aws_iam_role_policy.agentcore_runtime]
}

resource "aws_bedrockagentcore_agent_runtime" "tools" {
  count              = local.ac
  agent_runtime_name = "${local.ac_name}_tools"
  description        = "The MCP server's public tools (article 5), stateless streamable HTTP, behind the Gateway."
  role_arn           = aws_iam_role.agentcore_runtime[0].arn

  agent_runtime_artifact {
    code_configuration {
      entry_point = ["tools_main.py"]
      runtime     = "PYTHON_3_14"
      code {
        s3 {
          bucket = aws_s3_bucket.agentcore_code[0].id
          prefix = aws_s3_object.agentcore_zip[0].key
        }
      }
    }
  }

  network_configuration {
    network_mode = "PUBLIC"
  }
  protocol_configuration {
    server_protocol = "MCP"
  }
  lifecycle_configuration {
    idle_runtime_session_timeout = 60
    max_lifetime                 = 900
  }
  environment_variables = local.runtime_env

  depends_on = [aws_iam_role_policy.agentcore_runtime]
}

# --- Gateway: one MCP endpoint for other teams' clients, IAM-authenticated ---

resource "aws_iam_role" "agentcore_gateway" {
  count = local.ac
  name  = "${local.name}-agentcore-gateway"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "bedrock-agentcore.amazonaws.com" }
      Action    = "sts:AssumeRole"
      Condition = {
        StringEquals = { "aws:SourceAccount" = local.account_id }
        ArnLike      = { "aws:SourceArn" = "arn:aws:bedrock-agentcore:${var.region}:${local.account_id}:*" }
      }
    }]
  })
}

resource "aws_iam_role_policy" "agentcore_gateway" {
  count = local.ac
  role  = aws_iam_role.agentcore_gateway[0].id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid      = "CallTheToolsRuntime" # the only thing the Gateway can reach
      Effect   = "Allow"
      Action   = "bedrock-agentcore:InvokeAgentRuntime"
      Resource = [aws_bedrockagentcore_agent_runtime.tools[0].agent_runtime_arn, "${aws_bedrockagentcore_agent_runtime.tools[0].agent_runtime_arn}/*"]
    }]
  })
}

resource "aws_bedrockagentcore_gateway" "tools" {
  count           = local.ac
  name            = "${local.name}-tools"
  description     = "The CER reporting tools over MCP (article 7, D55). Callers sign with SigV4."
  role_arn        = aws_iam_role.agentcore_gateway[0].arn
  authorizer_type = "AWS_IAM"
  protocol_type   = "MCP"
}

resource "aws_bedrockagentcore_gateway_target" "tools" {
  count              = local.ac
  name               = "cer-tools"
  gateway_identifier = aws_bedrockagentcore_gateway.tools[0].gateway_id
  description        = "The tools Runtime; the Gateway signs each call with its role."

  credential_provider_configuration {
    gateway_iam_role {
      service = "bedrock-agentcore"
    }
  }

  target_configuration {
    mcp {
      mcp_server {
        endpoint = "https://bedrock-agentcore.${var.region}.amazonaws.com/runtimes/${urlencode(aws_bedrockagentcore_agent_runtime.tools[0].agent_runtime_arn)}/invocations?qualifier=DEFAULT"
      }
    }
  }

  depends_on = [aws_iam_role_policy.agentcore_gateway]
}

output "agentcore_agent_runtime_arn" {
  description = "AGENT_RUNTIME_ARN for the agent-nova-agentcore eval arm (null outside the window)."
  value       = one(aws_bedrockagentcore_agent_runtime.agent[*].agent_runtime_arn)
}

output "agentcore_gateway_url" {
  description = "GATEWAY_URL for python -m cer_agent.agentcore_client (null outside the window)."
  value       = one(aws_bedrockagentcore_gateway.tools[*].gateway_url)
}
