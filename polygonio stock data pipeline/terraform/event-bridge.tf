resource "aws_lambda_permission" "stock-ml-daily-stock-data" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.stock-ml-daily-stock-data.arn
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.stock-ml-daily-stock-data.arn
}

resource "aws_cloudwatch_event_rule" "stock-ml-daily-stock-data" {
  name = "stock-ml-daily-stock-data"
  description = "invoke stock-ml-daily-stock-data daily at 01:30 UTC"
  schedule_expression = "cron(30 1 ? * TUE-SAT *)"
}

resource "aws_cloudwatch_event_target" "daily-trigger-target" {
  arn = aws_lambda_function.stock-ml-daily-stock-data.arn
  rule = aws_cloudwatch_event_rule.stock-ml-daily-stock-data.name
}
