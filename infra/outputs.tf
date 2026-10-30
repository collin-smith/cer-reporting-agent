output "alerts_topic_arn" {
  value = aws_sns_topic.alerts.arn
}

output "budgets" {
  value = [aws_budgets_budget.monthly.name, aws_budgets_budget.series_total.name]
}

output "nova_lite_profile_arn" {
  description = "Call Nova Lite through this ARN so the spend is tagged."
  value       = aws_bedrock_inference_profile.nova_lite.arn
}
