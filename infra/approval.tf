# The approval gate (article 6, D51; brief §5.4, D25). Step Functions runs triage, then parks the case on a task
# token until a person approves, edits or rejects it from the CLI (`python -m cer_agent.approval`). An unanswered
# case escalates by SNS on D25's clock and, past its deadline, ends OVERDUE. Nothing is ever filed by the system.
#
# Build the Lambda package first:  .venv/bin/python scripts/build_lambda.py   (writes infra/build/approval.zip)
#
# Cost: nothing while idle (DynamoDB on demand, Lambda and Step Functions per use; logs kept 7 days). Per case:
# Standard workflow transitions $0.025 per 1,000, Lambda per GB-second, DynamoDB per request; a waiting case costs
# nothing while it waits (a token wait is one transition, however long). The model and guardrail calls dominate.

locals {
  lambda_zip = "${path.module}/build/approval.zip"
}

variable "approval_time_scale" {
  description = "Real seconds per scheduled minute for the escalation clock: 60 in production, 1 for a measured run."
  type        = number
  default     = 1
}

variable "approval_notify" {
  description = "on: escalations email the alerts topic; off: they are recorded on the case but not sent."
  type        = string
  default     = "on"
}

# --- Case record and review queue ---

resource "aws_dynamodb_table" "cases" {
  name         = "${local.name}-cases"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "case_id"

  attribute {
    name = "case_id"
    type = "S"
  }
  attribute {
    name = "status"
    type = "S"
  }
  attribute {
    name = "due_at"
    type = "S"
  }

  # The review queue: everything in one status, most urgent CER deadline first.
  global_secondary_index {
    name = "queue"
    key_schema { # hash_key / range_key on an index are deprecated in provider 6.71 (D61)
      attribute_name = "status"
      key_type       = "HASH"
    }
    key_schema {
      attribute_name = "due_at"
      key_type       = "RANGE"
    }
    projection_type    = "INCLUDE"
    non_key_attributes = ["deadline", "decision_status", "flags"]
  }
}

# --- Lambda: triage, park, escalate, close (one function, `step` in the event) ---

resource "aws_iam_role" "approval_lambda" {
  name = "${local.name}-approval-lambda"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{ Effect = "Allow", Principal = { Service = "lambda.amazonaws.com" }, Action = "sts:AssumeRole" }]
  })
}

resource "aws_iam_role_policy" "approval_lambda" {
  role = aws_iam_role.approval_lambda.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "NovaLiteThroughTheTaggedProfile"
        Effect = "Allow"
        Action = "bedrock:InvokeModel" # Converse is authorised as InvokeModel
        Resource = [
          aws_bedrock_inference_profile.nova_lite.arn,
          "arn:aws:bedrock:*:${local.account_id}:inference-profile/ca.amazon.nova-lite-v1:0",
          "arn:aws:bedrock:*::foundation-model/amazon.nova-lite-v1:0",
        ]
      },
      {
        # The fallback (D52, D54): only called when Nova Lite fails. Claude Haiku 4.5 through the tagged profile; the
        # US system profile behind it may serve the call from any US region, so its foundation models are listed too.
        Sid    = "FallbackHaikuThroughTheTaggedProfile"
        Effect = "Allow"
        Action = "bedrock:InvokeModel"
        Resource = [
          aws_bedrock_inference_profile.haiku45.arn,
          "arn:aws:bedrock:*:${local.account_id}:inference-profile/us.anthropic.claude-haiku-4-5-20251001-v1:0",
          "arn:aws:bedrock:*::foundation-model/anthropic.claude-haiku-4-5-20251001-v1:0",
        ]
      },
      {
        Sid      = "Guardrails"
        Effect   = "Allow"
        Action   = "bedrock:ApplyGuardrail"
        Resource = [aws_bedrock_guardrail.reports.guardrail_arn, aws_bedrock_guardrail.drafts.guardrail_arn]
      },
      {
        Sid      = "CaseRecord"
        Effect   = "Allow"
        Action   = ["dynamodb:PutItem", "dynamodb:UpdateItem", "dynamodb:GetItem"]
        Resource = aws_dynamodb_table.cases.arn
      },
      {
        Sid      = "Pages"
        Effect   = "Allow"
        Action   = "sns:Publish"
        Resource = aws_sns_topic.alerts.arn
      },
      {
        Sid      = "Logs"
        Effect   = "Allow"
        Action   = ["logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "${aws_cloudwatch_log_group.approval_lambda.arn}:*"
      },
    ]
  })
}

resource "aws_cloudwatch_log_group" "approval_lambda" {
  name              = "/aws/lambda/${local.name}-approval"
  retention_in_days = 7
}

resource "aws_lambda_function" "approval" {
  function_name    = "${local.name}-approval"
  role             = aws_iam_role.approval_lambda.arn
  runtime          = "python3.13"
  handler          = "cer_agent.approval.handler"
  filename         = local.lambda_zip
  source_code_hash = fileexists(local.lambda_zip) ? filebase64sha256(local.lambda_zip) : null
  memory_size      = 512
  timeout          = 120 # triage: three readings in parallel, the draft and two guardrail calls, with retries

  environment {
    variables = {
      MODEL_ARN          = aws_bedrock_inference_profile.nova_lite.arn
      FALLBACK_MODEL_ARN = aws_bedrock_inference_profile.haiku45.arn
      MODEL_RETRIES      = "3" # botocore retries per model: both chains fit the timeout (D52; 10 took up to 262 s)
      CER_PROMPT_CACHE   = "1" # cache the readers' tools + system prompt (D53: −32 to −49% a case, same answers)
      REPORTS_GUARDRAIL  = aws_bedrock_guardrail.reports.guardrail_id
      DRAFTS_GUARDRAIL   = aws_bedrock_guardrail.drafts.guardrail_id
      CASES_TABLE        = aws_dynamodb_table.cases.name
      TOPIC_ARN          = aws_sns_topic.alerts.arn
      TIME_SCALE         = tostring(var.approval_time_scale)
      NOTIFY             = var.approval_notify
      OBSERVABILITY      = var.observability_window ? "on" : "off" # spans and gate metrics to the logs (D58)
    }
  }

  # X-Ray traces each invocation during the observability window (D58); PassThrough is Lambda's default.
  tracing_config {
    mode = var.observability_window ? "Active" : "PassThrough"
  }

  # Inside private subnets only during the VPC hardening window (vpc.tf, D55); outside a VPC otherwise. The IDs
  # aren't known until the network exists, so the window goes up in two applies (network, then this change). Coming
  # down, the provider plans the empty lists but never sends them (D57): run scripts/vpc_detach.sh first.
  vpc_config {
    subnet_ids         = aws_subnet.private[*].id             # [] outside the window
    security_group_ids = aws_security_group.gate_lambda[*].id # [] outside the window
  }

  depends_on = [aws_cloudwatch_log_group.approval_lambda, aws_iam_role_policy_attachment.approval_lambda_vpc,
  aws_vpc_endpoint.interface, aws_iam_role_policy_attachment.approval_lambda_xray]
}

# --- Step Functions: triage -> wait for a person (escalating on timeout) -> close ---

resource "aws_iam_role" "approval_sfn" {
  name = "${local.name}-approval-sfn"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{ Effect = "Allow", Principal = { Service = "states.amazonaws.com" }, Action = "sts:AssumeRole" }]
  })
}

resource "aws_iam_role_policy" "approval_sfn" {
  role = aws_iam_role.approval_sfn.id
  policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{ Effect = "Allow", Action = "lambda:InvokeFunction", Resource = aws_lambda_function.approval.arn }]
  })
}

locals {
  invoke = "arn:aws:states:::lambda:invoke"
  retry_lambda = [{
    ErrorEquals     = ["Lambda.ServiceException", "Lambda.TooManyRequestsException", "Lambda.SdkClientException"]
    IntervalSeconds = 2
    MaxAttempts     = 3
    BackoffRate     = 2
  }]
}

resource "aws_sfn_state_machine" "approval" {
  name     = "${local.name}-approval"
  role_arn = aws_iam_role.approval_sfn.arn
  type     = "STANDARD"

  tracing_configuration {
    enabled = var.observability_window # X-Ray, observability window (D58)
  }

  definition = jsonencode({
    Comment = "CER triage: draft, then wait for a person; escalate on D25's clock; never file."
    StartAt = "Triage"
    States = {
      Triage = {
        Type       = "Task"
        Resource   = local.invoke
        Parameters = { FunctionName = aws_lambda_function.approval.arn, Payload = { step = "triage", "case_id.$" = "$.case_id", "report.$" = "$.report", "received.$" = "$.received", "operator.$" = "$.operator", "source.$" = "$.source", "elapsed_min.$" = "$.elapsed_min" } }
        OutputPath = "$.Payload"
        Retry      = local.retry_lambda
        # Any failure (a model error past its retries, a timeout, a bug) goes to a person, never nowhere.
        Catch = [{ ErrorEquals = ["States.ALL"], ResultPath = "$.error", Next = "TriageFailed" }]
        Next  = "WaitForApproval"
      }
      TriageFailed = {
        Type       = "Task"
        Resource   = local.invoke
        Parameters = { FunctionName = aws_lambda_function.approval.arn, Payload = { step = "triage_failed", "case_id.$" = "$.case_id", "report.$" = "$.report", "elapsed_min.$" = "$.elapsed_min", "error.$" = "$.error" } }
        OutputPath = "$.Payload"
        Retry      = local.retry_lambda
        Next       = "WaitForApproval"
      }
      WaitForApproval = {
        Type               = "Task"
        Resource           = "${local.invoke}.waitForTaskToken"
        Parameters         = { FunctionName = aws_lambda_function.approval.arn, Payload = { step = "park", "case.$" = "$", "token.$" = "$$.Task.Token" } }
        TimeoutSecondsPath = "$.wait_s"
        ResultPath         = "$.decision"
        Retry              = local.retry_lambda
        Catch              = [{ ErrorEquals = ["States.Timeout"], ResultPath = null, Next = "Escalate" }]
        Next               = "Close"
      }
      Escalate = {
        Type       = "Task"
        Resource   = local.invoke
        Parameters = { FunctionName = aws_lambda_function.approval.arn, Payload = { step = "escalate", "case.$" = "$" } }
        OutputPath = "$.Payload"
        Retry      = local.retry_lambda
        Next       = "Overdue?"
      }
      "Overdue?" = {
        Type    = "Choice"
        Choices = [{ Variable = "$.overdue", BooleanEquals = true, Next = "Overdue" }]
        Default = "WaitForApproval"
      }
      Overdue = { Type = "Fail", Error = "Overdue", Cause = "The reporting deadline passed with no approval." }
      Close = {
        Type       = "Task"
        Resource   = local.invoke
        Parameters = { FunctionName = aws_lambda_function.approval.arn, Payload = { step = "close", "case.$" = "$", "decision.$" = "$.decision" } }
        OutputPath = "$.Payload"
        Retry      = local.retry_lambda
        End        = true
      }
    }
  })

  depends_on = [aws_iam_role_policy.approval_sfn_xray]
}

output "approval_state_machine_arn" {
  value = aws_sfn_state_machine.approval.arn
}

output "cases_table" {
  value = aws_dynamodb_table.cases.name
}
