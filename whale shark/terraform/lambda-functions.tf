######################################################
# Lambda Function Properties

data "aws_s3_object" "env-var" {
  bucket = "do-terraform-1"
  key    = "secrets/whale-shark/env-variables.json"
}

data "terraform_remote_state" "lambda-layers" {
  backend = "s3"

  config = {
    bucket = "do-terraform-2"
    key    = "backends/lambda-layers/backend.tfstate"
    region = "us-east-2"
  }
}

######################################################
# Lambda Functions

resource "aws_lambda_function" "ws-word-count-update" {
  s3_bucket     = "do-terraform-1"
  s3_key        = "applications/whale-shark/lambda-functions/ws-word-count-update/package.zip"
  function_name = "ws-word-count-update"
  role          = aws_iam_role.whale-shark.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 90
  runtime = "python3.8"
  memory_size = "256"

  environment {
    variables = sensitive(jsondecode(data.aws_s3_object.env-var.body))
  }

  layers = [
    data.terraform_remote_state.lambda-layers.outputs.awswrangler-id
  ]
}

resource "aws_lambda_function" "ws-word-count-response" {
  s3_bucket     = "do-terraform-1"
  s3_key        = "applications/whale-shark/lambda-functions/ws-word-count-response/package.zip"
  function_name = "ws-word-count-response"
  role          = aws_iam_role.whale-shark.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 60
  runtime = "python3.8"
  memory_size = "256"

  environment {
    variables = sensitive(jsondecode(data.aws_s3_object.env-var.body))
  }

  layers = [
    data.terraform_remote_state.lambda-layers.outputs.awswrangler-id
    , data.terraform_remote_state.lambda-layers.outputs.requests-id
  ]
}




