# Article 7's observability window (D58): the smallest setup that lets the operator's team see the gate working and be
# told when it isn't. Off by default, like the other windows.
#
#   Traces   X-Ray active tracing on the state machine and the approval Lambda (service map, one trace per case run)
#            and the gate's own OpenTelemetry spans (triage, extract x3, decide, draft) written as JSON lines to the
#            Lambda's log group, queried with Logs Insights. Not Transaction Search: that is an account-wide switch.
#   Metrics  CER/Gate Overdue, Fallbacks, TriageFailed, by Embedded Metric Format from the same logs (no API calls),
#            plus the free AWS/Lambda and AWS/States metrics.
#   Watch    One dashboard; two alarms (any OVERDUE case, any fallback) to the alerts topic, which pages by email.
#
# On:  terraform apply -var observability_window=true      Off:  terraform apply   (one apply each way; no network)
# Cost (Price List, ca-central-1, 2026-11-12): custom metrics $0.30 per metric-month, prorated hourly, only for hours
# a metric is published; dashboard $3.00 a month, prorated hourly; alarms $0.10 each a month; X-Ray $5 per million
# traces stored; logs $0.55/GB in. Free tier: 10 metrics, 3 dashboards, 10 alarms, 100k traces a month. Idle with
# the window on: dashboard + alarms, $0 inside the free tier, $3.20 a month outside it.

variable "observability_window" {
  description = "Article 7's observability window (D58): traces, gate metrics, a dashboard and two alarms."
  type        = bool
  default     = false
}

locals {
  obs     = var.observability_window ? 1 : 0
  obs_ns  = "CER/Gate"
  obs_log = aws_cloudwatch_log_group.approval_lambda.name
}

# X-Ray: the Lambda's role writes its segments (active tracing); the state machine's role writes its own.
resource "aws_iam_role_policy_attachment" "approval_lambda_xray" {
  count      = local.obs
  role       = aws_iam_role.approval_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess"
}

resource "aws_iam_role_policy" "approval_sfn_xray" {
  count = local.obs
  name  = "xray"
  role  = aws_iam_role.approval_sfn.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["xray:PutTraceSegments", "xray:PutTelemetryRecords", "xray:GetSamplingRules", "xray:GetSamplingTargets"]
      Resource = "*" # X-Ray actions have no resource-level permissions
    }]
  })
}

# --- Alarms: any OVERDUE case, any fallback; both page the alerts topic ---
# No ok_actions: on every switch-on each alarm emailed an "OK" as it left INSUFFICIENT_DATA (D58).

resource "aws_cloudwatch_metric_alarm" "overdue" {
  count               = local.obs
  alarm_name          = "${local.name}-gate-overdue"
  alarm_description   = "A case passed its CER deadline with no approval. File by hand now: python -m cer_agent.approval queue"
  namespace           = local.obs_ns
  metric_name         = "Overdue"
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  threshold           = 1
  comparison_operator = "GreaterThanOrEqualToThreshold"
  treat_missing_data  = "notBreaching" # no metric means no overdue case
  alarm_actions       = [aws_sns_topic.alerts.arn]
}

resource "aws_cloudwatch_metric_alarm" "fallbacks" {
  count               = local.obs
  alarm_name          = "${local.name}-gate-fallbacks"
  alarm_description   = "Nova Lite failed and the gate used Haiku 4.5 or the rules alone. Check Bedrock health and the case's flags."
  namespace           = local.obs_ns
  metric_name         = "Fallbacks"
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  threshold           = 1
  comparison_operator = "GreaterThanOrEqualToThreshold"
  treat_missing_data  = "notBreaching"
  alarm_actions       = [aws_sns_topic.alerts.arn]
}

# --- Dashboard: what the operator's team looks at (12 metrics; the free tier allows 50) ---
# The cases table shows usd_per_1000 (cost x 1,000, floored to 3 places): raw cost_usd mixed 9.3E-4 with 0.001056 (D58).

resource "aws_cloudwatch_dashboard" "gate" {
  count          = local.obs
  dashboard_name = "${local.name}-gate"
  dashboard_body = jsonencode({
    widgets = [
      {
        type       = "text", x = 0, y = 0, width = 24, height = 2
        properties = { markdown = "## CER triage gate\nCases in, how long triage takes, what failed or fell back, and what each case cost. Alarms page the alerts topic. Runbook: article 7." }
      },
      {
        type = "metric", x = 0, y = 2, width = 8, height = 6
        properties = {
          title = "Case runs (Step Functions)", region = var.region, stat = "Sum", period = 300, view = "timeSeries"
          metrics = [
            ["AWS/States", "ExecutionsStarted", "StateMachineArn", aws_sfn_state_machine.approval.arn],
            [".", "ExecutionsSucceeded", ".", "."],
            [".", "ExecutionsFailed", ".", ".", { label = "ExecutionsFailed (OVERDUE ends here)" }],
          ]
        }
      },
      {
        type = "metric", x = 8, y = 2, width = 8, height = 6
        properties = {
          title = "Gate Lambda: time per step", region = var.region, period = 300, view = "timeSeries"
          metrics = [
            ["AWS/Lambda", "Duration", "FunctionName", aws_lambda_function.approval.function_name, { stat = "p50" }],
            ["...", { stat = "p95" }],
            ["...", { stat = "Maximum" }],
          ]
        }
      },
      {
        type = "metric", x = 16, y = 2, width = 8, height = 6
        properties = {
          title = "Needs a person", region = var.region, stat = "Sum", period = 300, view = "timeSeries"
          metrics = [
            [local.obs_ns, "Overdue"],
            [".", "Fallbacks"],
            [".", "TriageFailed"],
            ["AWS/Lambda", "Errors", "FunctionName", aws_lambda_function.approval.function_name],
            [".", "Invocations", ".", ".", { visible = false }],
          ]
        }
      },
      {
        type = "log", x = 0, y = 8, width = 12, height = 7
        properties = {
          title = "Cases triaged: decision, deadline, time and AI cost ($ per 1,000 such reports)", region = var.region, view = "table"
          query = "SOURCE '${local.obs_log}' | filter ispresent(cost_usd) | fields @timestamp, case_id, status, deadline, seconds, floor(cost_usd * 1000000) / 1000 as usd_per_1000, drafted_by, Fallbacks | sort @timestamp desc | limit 50"
        }
      },
      {
        type = "log", x = 12, y = 8, width = 12, height = 7
        properties = {
          title = "Where triage time goes (gate spans)", region = var.region, view = "table"
          query = "SOURCE '${local.obs_log}' | filter ispresent(cer_span) | stats count() as spans, pct(duration_ms, 50) as p50_ms, pct(duration_ms, 95) as p95_ms, sum(status = 'ERROR') as errors by name | sort p95_ms desc"
        }
      },
      {
        type = "alarm", x = 0, y = 15, width = 24, height = 2
        properties = {
          title  = "Alarms"
          alarms = [aws_cloudwatch_metric_alarm.overdue[0].arn, aws_cloudwatch_metric_alarm.fallbacks[0].arn]
        }
      },
    ]
  })
}

output "observability_dashboard" {
  value = var.observability_window ? "https://${var.region}.console.aws.amazon.com/cloudwatch/home?region=${var.region}#dashboards/dashboard/${local.name}-gate" : null
}
