# Cost guardrails (D6, D11). Two budgets, both filtered to spend tagged project=<var.project>:
#
#   1. monthly: emails at $50 and $75, and at $100 (the teardown line). The Budgets action that enforces the $100
#      stop is added with the first IAM role the pipeline runs as: an action needs a role to attach its deny
#      policy to, and in week 1 everything runs locally under the developer's own credentials.
#   2. series_total: the $300 cap for the whole series, cumulative from var.series_start.
#
# The account is shared (StudySite; formerly MLOps). It already has an account-wide budget, so this stack adds
# none, and the tag filter keeps other projects' spend from tripping these alerts.
#
# Both count usage BEFORE credits (include_credit = false). The account is on the AWS Free plan, which books
# usage as a charge plus an equal negative credit, so a budget on default settings reads $0 and never fires.
#
# Cost: budgets without actions are free. The tag key `project` is already an active cost-allocation tag in this
# account.

resource "aws_budgets_budget" "monthly" {
  name         = "${local.name}-monthly"
  budget_type  = "COST"
  limit_amount = tostring(var.monthly_stop_usd)
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  # format() rather than "...$${...}", which HCL would read as an escaped interpolation.
  cost_filter {
    name   = "TagKeyValue"
    values = [format("user:project$%s", var.project)]
  }

  cost_types {
    include_credit = false
  }

  dynamic "notification" {
    for_each = concat(var.monthly_alerts_usd, [var.monthly_stop_usd])
    content {
      comparison_operator        = "GREATER_THAN"
      threshold                  = notification.value
      threshold_type             = "ABSOLUTE_VALUE"
      notification_type          = "ACTUAL"
      subscriber_email_addresses = [var.alert_email]
      subscriber_sns_topic_arns  = [aws_sns_topic.alerts.arn]
    }
  }
}

resource "aws_budgets_budget" "series_total" {
  name              = "${local.name}-series-total"
  budget_type       = "COST"
  limit_amount      = tostring(var.series_cap_usd)
  limit_unit        = "USD"
  time_unit         = "ANNUALLY"
  time_period_start = var.series_start

  cost_filter {
    name   = "TagKeyValue"
    values = [format("user:project$%s", var.project)]
  }

  cost_types {
    include_credit = false
  }

  dynamic "notification" {
    for_each = [50, 80, 100]
    content {
      comparison_operator        = "GREATER_THAN"
      threshold                  = notification.value
      threshold_type             = "PERCENTAGE"
      notification_type          = "ACTUAL"
      subscriber_email_addresses = [var.alert_email]
      subscriber_sns_topic_arns  = [aws_sns_topic.alerts.arn]
    }
  }
}
