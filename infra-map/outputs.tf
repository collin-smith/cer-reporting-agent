output "url" {
  description = "The public address of the map."
  value       = "https://${aws_cloudfront_distribution.page.domain_name}/"
}

output "bucket" {
  value = aws_s3_bucket.page.id
}

output "distribution_id" {
  description = "For cache invalidation after re-uploading the page (scripts/deploy_map.sh)."
  value       = aws_cloudfront_distribution.page.id
}
