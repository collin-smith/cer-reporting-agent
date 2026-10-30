variable "region" {
  description = "Everything runs in Canada (Central). Claude models are reached through us./global. inference profiles."
  type        = string
  default     = "ca-central-1"
}

variable "project" {
  description = "Resource name prefix and cost-allocation tag value (tag key: project)."
  type        = string
  default     = "agentic-ai"
}

variable "alert_email" {
  description = "Address that receives budget and alarm notifications."
  type        = string
}

variable "series_start" {
  description = "Start of the series-total budget period (first of a month, YYYY-MM-DD_HH:MM)."
  type        = string
  default     = "2026-10-01_00:00"
}

variable "series_cap_usd" {
  description = "Series cap: total spend tagged to this project over the whole series (D6, D11)."
  type        = number
  default     = 300
}

variable "monthly_stop_usd" {
  description = "Monthly spend tagged to this project at which everything is torn down (D6, D11)."
  type        = number
  default     = 100
}

variable "monthly_alerts_usd" {
  description = "Monthly spend tagged to this project that triggers a warning email (D6, D11)."
  type        = list(number)
  default     = [50, 75]
}
