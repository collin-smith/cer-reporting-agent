variable "region" {
  type    = string
  default = "ca-central-1"
}

variable "project" {
  description = "Cost-allocation tag. Not agentic-ai: the map outlives the series, and nuke.sh only touches agentic-ai."
  type        = string
  default     = "cer-incident-map"
}

variable "bucket_name" {
  description = "S3 bucket for the page. Global across AWS; the public never sees it (OAC). No cer- prefix: it isn't a CER site."
  type        = string
  default     = "pipeline-incident-map-2026"
}
