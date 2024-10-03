/*
resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ws-word-count-update.arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.whale-shark.arn
}

resource "aws_s3_bucket_notification" "s3-trigger" {
  bucket = aws_s3_bucket.whale-shark.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.ws-word-count-update.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "events-v2/"
  }
}
*/

resource "aws_lambda_permission" "allow-eventbridge" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ws-word-count-update.arn
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.daily-trigger.arn
}


resource "aws_cloudwatch_event_rule" "daily-trigger" {
  name = "ws-word-count-update_daily-trigger"
  description = "invoke ws-word-count-update daily"
  schedule_expression = "cron(5 0 * * ? *)"
}

resource "aws_cloudwatch_event_target" "daily-trigger-target" {
  arn = aws_lambda_function.ws-word-count-update.arn
  rule = aws_cloudwatch_event_rule.daily-trigger.name
}
