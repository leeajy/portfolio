data "aws_s3_object" "stock-ml-daily-stock-data" {
  bucket = "do-terraform-1"
  key    = "applications/stock-ml/step-functions/stock-ml-daily-stock-data.json"
}

resource "aws_sfn_state_machine" "stock-ml-daily-stock-data" {
  name     = "stock-ml-daily-stock-data"
  role_arn = aws_iam_role.stock-ml.arn

  definition = data.aws_s3_object.stock-ml-daily-stock-data.body
  logging_configuration {
    include_execution_data = false
    level                  = "OFF"
  }
}
