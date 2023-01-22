# Niches Lambda
resource "aws_lambda_permission" "apigw_lambda_gyms" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.Gyms.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.WorkoutsApi.id}/*/*"
}

resource "aws_lambda_function" "Gyms" {
  filename         = "../GymFunction/main.zip"
  function_name    = "${var.prefix}_gyms"
  description      = "Create, Edit, and Return Lists of Gyms"
  role             = aws_iam_role.WorkoutsLambdaRole.arn
  memory_size      = 512
  timeout          = 20
  package_type     = "Zip"
  publish          = false
  handler          = "main"
  runtime          = "go1.x"
  source_code_hash = filebase64sha256("../GymFunction/main.zip")
  environment {
    variables = {
      DB_HOST     = aws_db_instance.DB.address
      DB_USER     = aws_db_instance.DB.username
      DB_PASSWORD = data.aws_ssm_parameter.db_password.value
      DB_NAME     = aws_db_instance.DB.name
    }
  }
  vpc_config {
    subnet_ids         = tolist(data.aws_subnet_ids.public.ids)
    security_group_ids = [aws_security_group.WorkoutsSecurityGroup.id]
  }
}
