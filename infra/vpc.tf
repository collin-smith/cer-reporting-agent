# Article 7's VPC hardening window (D55): the approval Lambda moved into private subnets with no route to the
# internet, reaching AWS only through VPC endpoints. Built, measured and torn down the same day; off by default.
#
# What the Lambda calls, and how it gets there inside the VPC:
#   Bedrock runtime (Nova Lite, the guardrails, the Haiku 4.5 fallback)   interface endpoint, private DNS
#   SNS (escalation pages)                                                  interface endpoint, private DNS
#   DynamoDB (the case record)                                              gateway endpoint (free)
#   CloudWatch Logs                                                         none: Lambda ships its logs itself
#   Step Functions                                                          none: only the approver CLI calls it
# No NAT gateway: with no route out, a report can't leave AWS from the function, whatever text it carries.
#
# On:   two applies with -var vpc_window=true (the network first, then the Lambda joins it).
# Off:  ./scripts/vpc_detach.sh, which must report the Lambda outside any VPC, THEN terraform apply (default false).
# Cost (Price List, ca-central-1): interface endpoints $0.011 per hour per AZ + $0.01 per GB, so 2 endpoints x 2 AZs
# = $0.044 an hour ($32 a month if left up: hence the window). VPC, subnets, route table, security groups and the
# DynamoDB gateway endpoint are free.
#
# Why the CLI step (D57): the plan shows vpc_config's lists going to [], but hashicorp/aws 6.71.0 never sends that
# update (CloudTrail, 2026-11-11). A plain apply then deletes the endpoints while the Lambda is still inside, cutting
# it off from Bedrock and SNS, and times out after 45 minutes on the subnets its network interfaces still hold.
# Detached by the CLI, the interfaces were released in under a minute and the apply finished in seconds.

variable "vpc_window" {
  description = "Article 7's VPC hardening window (D55): true moves the approval Lambda into private subnets."
  type        = bool
  default     = false
}

locals {
  vpc = var.vpc_window ? 1 : 0
}

data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_vpc" "gate" {
  count                = local.vpc
  cidr_block           = "10.42.0.0/16"
  enable_dns_support   = true # both needed for the endpoints' private DNS names
  enable_dns_hostnames = true
  tags                 = { Name = "${local.name}-gate" }
}

resource "aws_subnet" "private" {
  count             = local.vpc * 2 # two AZs, as the Lambda service recommends
  vpc_id            = aws_vpc.gate[0].id
  cidr_block        = cidrsubnet("10.42.0.0/16", 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  tags              = { Name = "${local.name}-private-${count.index}" }

  timeouts {
    delete = "45m" # waits for the Lambda's network interfaces to be released
  }
}

resource "aws_route_table" "private" {
  count  = local.vpc
  vpc_id = aws_vpc.gate[0].id
  tags   = { Name = "${local.name}-private" } # no default route: nothing leaves the VPC
}

resource "aws_route_table_association" "private" {
  count          = local.vpc * 2
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[0].id
}

resource "aws_security_group" "gate_lambda" {
  count       = local.vpc
  name        = "${local.name}-gate-lambda"
  description = "The approval Lambda: HTTPS out to the VPC endpoints and DynamoDB only"
  vpc_id      = aws_vpc.gate[0].id

  timeouts {
    delete = "45m"
  }
}

resource "aws_security_group" "endpoints" {
  count       = local.vpc
  name        = "${local.name}-endpoints"
  description = "Interface endpoints: HTTPS in from the approval Lambda only"
  vpc_id      = aws_vpc.gate[0].id
}

resource "aws_vpc_security_group_ingress_rule" "endpoints_from_lambda" {
  count                        = local.vpc
  security_group_id            = aws_security_group.endpoints[0].id
  referenced_security_group_id = aws_security_group.gate_lambda[0].id
  ip_protocol                  = "tcp"
  from_port                    = 443
  to_port                      = 443
}

resource "aws_vpc_security_group_egress_rule" "lambda_to_endpoints" {
  count                        = local.vpc
  security_group_id            = aws_security_group.gate_lambda[0].id
  referenced_security_group_id = aws_security_group.endpoints[0].id
  ip_protocol                  = "tcp"
  from_port                    = 443
  to_port                      = 443
}

resource "aws_vpc_security_group_egress_rule" "lambda_to_dynamodb" {
  count             = local.vpc
  security_group_id = aws_security_group.gate_lambda[0].id
  prefix_list_id    = aws_vpc_endpoint.dynamodb[0].prefix_list_id
  ip_protocol       = "tcp"
  from_port         = 443
  to_port           = 443
}

resource "aws_vpc_endpoint" "interface" {
  for_each            = var.vpc_window ? toset(["bedrock-runtime", "sns"]) : toset([])
  vpc_id              = aws_vpc.gate[0].id
  service_name        = "com.amazonaws.${var.region}.${each.key}"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = aws_subnet.private[*].id
  security_group_ids  = [aws_security_group.endpoints[0].id]
  private_dns_enabled = true
  tags                = { Name = "${local.name}-${each.key}" }
}

resource "aws_vpc_endpoint" "dynamodb" {
  count             = local.vpc
  vpc_id            = aws_vpc.gate[0].id
  service_name      = "com.amazonaws.${var.region}.dynamodb"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [aws_route_table.private[0].id]
  tags              = { Name = "${local.name}-dynamodb" }
}

# The Lambda needs to create and delete its network interfaces in the subnets.
resource "aws_iam_role_policy_attachment" "approval_lambda_vpc" {
  count      = local.vpc
  role       = aws_iam_role.approval_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}
