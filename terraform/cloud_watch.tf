resource "aws_cloudwatch_event_rule" "exchange_rate_fetcher_event" {
  name                = "CurrencyFetcherEvent"
  description         = "Triggers exchange rate fetcher function on a schedule"
  schedule_expression = var.exchange_rate_fetcher_scedule
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.exchange_rate_fetcher_event.name
  target_id = "ScheduleExchangeRateFetcherLambda"
  arn       = aws_lambda_function.exchange_rate_fetcher_lambda.arn
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowCloudWatchEventsInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.exchange_rate_fetcher_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.exchange_rate_fetcher_event.arn
}
