data "archive_file" "currency_informer_lambda_logslambda_zip_file" {
  output_path = "${path.module}/../lambdas/currency_informer.zip"
  source_dir  = "${path.module}/../lambdas/currency_informer"
  excludes    = ["__pycache__", "*.pyc"]
  type        = "zip"
}

resource "aws_lambda_function" "currency_informer_lambda" {
  filename         = "${path.module}/../lambdas/currency_informer.zip"
  function_name    = "currency-informer"
  role             = aws_iam_role.currency_informer_lambda_iam_role.arn
  handler          = "currency_informer.handler"
  source_code_hash = data.archive_file.currency_informer_lambda_logslambda_zip_file.output_base64sha256
  runtime          = local.lambda_python_version
  layers           = [aws_lambda_layer_version.common_lambda_layer.arn]
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.currency_history_table.name
    }
  }
}

resource "aws_iam_role" "currency_informer_lambda_iam_role" {
  name               = "currency-informer-lambda-iam-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_cloudwatch_log_group" "currency_informer_lambda_log_group" {
  name              = "/aws/lambdas/currency_informer"
  retention_in_days = local.lambda_retention_in_days
}


resource "aws_iam_role_policy_attachment" "currency_informer_lambda_policy" {
  role       = aws_iam_role.currency_informer_lambda_iam_role.name
  policy_arn = aws_iam_policy.lambda_log_policy.arn
}


resource "aws_iam_role_policy" "currency_informer_lambda_iam_policy" {
  name   = "currency-informer-lambda-iam-policy"
  role   = aws_iam_role.currency_informer_lambda_iam_role.name
  policy = data.aws_iam_policy_document.currency_informer_lambda_iam_policy_document.json
}

data "aws_iam_policy_document" "currency_informer_lambda_iam_policy_document" {
  version = "2012-10-17"

  statement {
    effect = "Allow"
    actions = [
      "dynamodb:Query",
    ]
    resources = [
      aws_dynamodb_table.currency_history_table.arn
    ]
  }

}
