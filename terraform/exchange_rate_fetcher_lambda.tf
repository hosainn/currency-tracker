data "archive_file" "exchange_rate_fetcher_lambda_zip_file" {
  output_path = "${path.module}/../lambdas/exchange_rate_fetcher.zip"
  source_dir  = "${path.module}/../lambdas/exchange_rate_fetcher"
  excludes    = ["__pycache__", "*.pyc"]
  type        = "zip"
}

resource "aws_lambda_function" "exchange_rate_fetcher_lambda" {
  filename         = "${path.module}/../lambdas/exchange_rate_fetcher.zip"
  function_name    = "exchange-rate-fetcher"
  role             = aws_iam_role.exchange_rate_fetcher_laambda_iam_role.arn
  handler          = "exchange_rate_fetcher.handler"
  source_code_hash = data.archive_file.exchange_rate_fetcher_lambda_zip_file.output_base64sha256
  runtime          = local.lambda_python_version
  layers           = [aws_lambda_layer_version.common_lambda_layer.arn]
  environment {
    variables = {
      TABLE_NAME             = aws_dynamodb_table.currency_history_table.name
      ECB_NAMESPACE_URL      = var.ecb_namespace
      ECB_EXCHANGE_RATES_URL = var.ecb_exchange_rates_url
    }
  }
}

resource "aws_iam_role" "exchange_rate_fetcher_laambda_iam_role" {
  name               = "exchange-rate-fetcher-lambda-iam-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_cloudwatch_log_group" "exchange_rate_fetcher_laambda_log_group" {
  name              = "/aws/lambdas/exchange_rate_fetcher"
  retention_in_days = local.lambda_retention_in_days
}


resource "aws_iam_role_policy_attachment" "exchange_rate_fetcher_lambda_policy" {
  role       = aws_iam_role.exchange_rate_fetcher_laambda_iam_role.name
  policy_arn = aws_iam_policy.lambda_log_policy.arn
}

resource "aws_iam_role_policy" "exchange_rate_fetcher_lambda_policy" {
  name   = "exchange-rate-fetcher-lambda-policy"
  role   = aws_iam_role.exchange_rate_fetcher_laambda_iam_role.name
  policy = data.aws_iam_policy_document.exchange_rate_fetcher_lambda_policy_document.json
}

data "aws_iam_policy_document" "exchange_rate_fetcher_lambda_policy_document" {
  version = "2012-10-17"

  statement {
    effect = "Allow"
    actions = [
      "dynamodb:PutItem",
    ]
    resources = [
      aws_dynamodb_table.currency_history_table.arn
    ]
  }

}
