resource "aws_api_gateway_rest_api" "WorkoutsApi" {
  name = "${var.prefix}_api"
}


## RESOURCES AND METHODS
resource "aws_api_gateway_resource" "GymsPath" {
  parent_id   = aws_api_gateway_rest_api.WorkoutsApi.root_resource_id
  path_part   = "gyms"
  rest_api_id = aws_api_gateway_rest_api.WorkoutsApi.id
}

resource "aws_api_gateway_resource" "GymsPath" {
  parent_id   = aws_api_gateway_rest_api.WorkoutsApi.root_resource_id
  path_part   = "gyms"
  rest_api_id = aws_api_gateway_rest_api.WorkoutsApi.id
}

resource "aws_api_gateway_method" "GetGyms" {
  authorization    = "NONE"
  http_method      = "GET"
  resource_id      = aws_api_gateway_resource.GymsPath.id
  rest_api_id      = aws_api_gateway_rest_api.WorkoutsApi.id
  api_key_required = true
}

resource "aws_api_gateway_method" "PostGyms" {
  authorization    = "NONE"
  http_method      = "POST"
  resource_id      = aws_api_gateway_resource.GymsPath.id
  rest_api_id      = aws_api_gateway_rest_api.WorkoutsApi.id
  api_key_required = true
}


## INTEGRATIONS 
resource "aws_api_gateway_integration" "GetGymsLambdaIntegration" {
  rest_api_id             = aws_api_gateway_rest_api.WorkoutsApi.id
  resource_id             = aws_api_gateway_resource.GymsPath.id
  http_method             = aws_api_gateway_method.GetGyms.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.Gyms.invoke_arn
}
resource "aws_api_gateway_integration" "PostGymsLambdaIntegration" {
  rest_api_id             = aws_api_gateway_rest_api.WorkoutsApi.id
  resource_id             = aws_api_gateway_resource.GymsPath.id
  http_method             = aws_api_gateway_method.PostGyms.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.Gyms.invoke_arn
}

## STAGE AND DEPLOYMENT

resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.WorkoutsApi.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.GymsPath,
      aws_api_gateway_method.GetGyms,
      aws_api_gateway_method.PostGyms,
      aws_api_gateway_integration.GetGymsLambdaIntegration,
      aws_api_gateway_integration.PostGymsLambdaIntegration,
      module.gyms-enable-cors,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "stage" {
  deployment_id = aws_api_gateway_deployment.deployment.id
  rest_api_id   = aws_api_gateway_rest_api.WorkoutsApi.id
  stage_name    = var.prefix
}

//CORS Headers
module "gyms-enable-cors" {
  source          = "squidfunk/api-gateway-enable-cors/aws"
  version         = "0.3.3"
  api_id          = aws_api_gateway_rest_api.WorkoutsApi.id
  api_resource_id = aws_api_gateway_resource.GymsPath.id
}
