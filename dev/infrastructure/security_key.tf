resource "aws_api_gateway_api_key" "ExtensionKey" {
  name    = "${var.prefix}_ext_key"
  enabled = true
}

resource "aws_api_gateway_usage_plan" "UsagePlan" {
  name        = "${var.prefix}_usage_plan"
  description = "Plan to Manage ${var.prefix} extension keys"

  api_stages {
    api_id = aws_api_gateway_rest_api.WorkoutsApi.id
    stage  = aws_api_gateway_stage.stage.stage_name
  }
}

resource "aws_api_gateway_usage_plan_key" "main" {
  key_id        = aws_api_gateway_api_key.ExtensionKey.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.UsagePlan.id
}
