resource "aws_api_gateway_rest_api" "currency_api" {
  name        = "CurrencyInfoAPI"
  description = "API to fetch currency information"
}

resource "aws_api_gateway_resource" "currency_resource" {
  rest_api_id = aws_api_gateway_rest_api.currency_api.id
  parent_id   = aws_api_gateway_rest_api.currency_api.root_resource_id
  path_part   = "currency"
}

resource "aws_api_gateway_method" "get_currency" {
  rest_api_id   = aws_api_gateway_rest_api.currency_api.id
  resource_id   = aws_api_gateway_resource.currency_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.currency_api.id
  resource_id = aws_api_gateway_resource.currency_resource.id
  http_method = aws_api_gateway_method.get_currency.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.currency_informer_lambda.invoke_arn
}

resource "aws_api_gateway_deployment" "api_deployment" {
  depends_on = [aws_api_gateway_integration.lambda_integration]

  rest_api_id = aws_api_gateway_rest_api.currency_api.id
  stage_name  = "test"
}


resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.currency_informer_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.currency_api.execution_arn}/*/*"
}

output "base_url" {
  value = aws_api_gateway_deployment.api_deployment.invoke_url
}
