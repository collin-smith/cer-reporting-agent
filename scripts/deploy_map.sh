#!/usr/bin/env bash
# Upload the incident map to its bucket and clear CloudFront's cache (code/infra-map/).
# Run from code/ after `terraform -chdir=infra-map apply`. Rebuild the page first if the data or links changed:
#   python3 -I scripts/build_map.py
set -euo pipefail
cd "$(dirname "$0")/.."
PAGE=../output/cer-incident-map.html
BUCKET=$(terraform -chdir=infra-map output -raw bucket)
DIST=$(terraform -chdir=infra-map output -raw distribution_id)
aws s3 cp "$PAGE" "s3://${BUCKET}/index.html" \
  --content-type "text/html; charset=utf-8" --cache-control "public, max-age=300"
aws cloudfront create-invalidation --distribution-id "$DIST" --paths "/index.html" "/" --query Invalidation.Id --output text
echo "Live at $(terraform -chdir=infra-map output -raw url)"
