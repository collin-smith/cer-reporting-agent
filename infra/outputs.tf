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

output "haiku_profile_arn" {
  description = "Call Claude Haiku 5.5 through this ARN so the spend is tagged."
  value       = aws_bedrock_inference_profile.haiku.arn
}

output "writer_profile_arns" {
  description = "Synthetic-report writers (D27); call them through these ARNs so the spend is tagged."
  value = {
    llama   = aws_bedrock_inference_profile.writer_llama.arn
    mistral = aws_bedrock_inference_profile.writer_mistral.arn
  }
}


output "nova_pro_profile_arn" {
  description = "Call Nova Pro (judge comparison D36) through this ARN so the spend is tagged."
  value       = aws_bedrock_inference_profile.nova_pro.arn
}

output "guardrail_id" {
  description = "Detect-mode report guardrail (article 6); used by python -m cer_agent.guard as GUARDRAIL_ID."
  value       = aws_bedrock_guardrail.reports.guardrail_id
}
