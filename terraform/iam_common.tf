resource "aws_iam_policy" "lambda_log_policy" {
  name        = "lambda-log-policy"
  description = "IAM policy to grant AWS Lambda functions permission to create and manage CloudWatch log groups and log streams, as well as to put log events for monitoring and troubleshooting purposes."
  policy      = data.aws_iam_policy_document.lambda_log_policy.json
}

data "aws_iam_policy_document" "lambda_log_policy" {
  version = "2012-10-17"

  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["arn:aws:logs:*:*:*"]
  }
}
