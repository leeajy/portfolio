######################################################
# Lambda Function Properties

data "aws_s3_object" "env-var" {
  bucket = "do-terraform-1"
  key    = "secrets/stock-ml/env-variables.json"
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
resource "aws_lambda_function" "stock-ml-daily-stock-data" {
  s3_bucket     = "do-terraform-1"
  s3_key        = "applications/stock-ml/lambda-functions/stock-ml-daily-stock-data/package.zip"
  function_name = "stock-ml-daily-stock-data"
  role          = aws_iam_role.stock-ml.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 600
  runtime = "python3.8"
  memory_size = "128"

  environment {
    variables = sensitive(jsondecode(data.aws_s3_object.env-var.body))
  }

  layers = [
  ]
}


resource "aws_lambda_function" "stock-ml-check-market-open" {
  s3_bucket     = "do-terraform-1"
  s3_key        = "applications/stock-ml/lambda-functions/stock-ml-check-market-open/package.zip"
  function_name = "stock-ml-check-market-open"
  role          = aws_iam_role.stock-ml.arn
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

resource "aws_lambda_function" "stock-ml-daily-open-close" {
  s3_bucket     = "do-terraform-1"
  s3_key        = "applications/stock-ml/lambda-functions/stock-ml-daily-open-close/package.zip"
  function_name = "stock-ml-daily-open-close"
  role          = aws_iam_role.stock-ml.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 60
  runtime = "python3.8"
  memory_size = "256"

  environment {
    variables = sensitive(jsondecode(data.aws_s3_object.env-var.body))
  }

  layers = [
    local.layer-stock-ml
    , data.terraform_remote_state.lambda-layers.outputs.pandas-id
    , data.terraform_remote_state.lambda-layers.outputs.requests-id
  ]
}

resource "aws_lambda_function" "stock-ml-get-ticker-api" {
  s3_bucket     = "do-terraform-1"
  s3_key        = "applications/stock-ml/lambda-functions/stock-ml-get-ticker-api/package.zip"
  function_name = "stock-ml-get-ticker-api"
  role          = aws_iam_role.stock-ml.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 60
  runtime = "python3.8"
  memory_size = "128"

  environment {
    variables = sensitive(jsondecode(data.aws_s3_object.env-var.body))
  }

  layers = [
    data.terraform_remote_state.lambda-layers.outputs.pandas-id
    , data.terraform_remote_state.lambda-layers.outputs.requests-id
  ]
}

resource "aws_lambda_function" "stock-ml-get-ticker-series" {
  s3_bucket     = "do-terraform-1"
  s3_key        = "applications/stock-ml/lambda-functions/stock-ml-get-ticker-series/package.zip"
  function_name = "stock-ml-get-ticker-series"
  role          = aws_iam_role.stock-ml.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 60
  runtime = "python3.8"
  memory_size = "128"

  environment {
    variables = sensitive(jsondecode(data.aws_s3_object.env-var.body))
  }

  layers = [
    data.terraform_remote_state.lambda-layers.outputs.pandas-id
    , data.terraform_remote_state.lambda-layers.outputs.requests-id
  ]
}

resource "aws_lambda_function" "stock-ml-get-ema" {
  s3_bucket     = "do-terraform-1"
  s3_key        = "applications/stock-ml/lambda-functions/stock-ml-get-ema/package.zip"
  function_name = "stock-ml-get-ema"
  role          = aws_iam_role.stock-ml.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 60
  runtime = "python3.8"
  memory_size = "128"

  environment {
    variables = sensitive(jsondecode(data.aws_s3_object.env-var.body))
  }

  layers = [
    local.layer-stock-ml
    , data.terraform_remote_state.lambda-layers.outputs.pandas-id
    , data.terraform_remote_state.lambda-layers.outputs.requests-id
  ]
}

resource "aws_lambda_function" "stock-ml-get-news" {
  s3_bucket     = "do-terraform-1"
  s3_key        = "applications/stock-ml/lambda-functions/stock-ml-get-news/package.zip"
  function_name = "stock-ml-get-news"
  role          = aws_iam_role.stock-ml.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 60
  runtime = "python3.8"
  memory_size = "128"

  environment {
    variables = sensitive(jsondecode(data.aws_s3_object.env-var.body))
  }

  layers = [
    local.layer-stock-ml
    , data.terraform_remote_state.lambda-layers.outputs.pandas-id
    , data.terraform_remote_state.lambda-layers.outputs.requests-id
  ]
}

resource "aws_lambda_function" "stock-ml-get-rsi" {
  s3_bucket     = "do-terraform-1"
  s3_key        = "applications/stock-ml/lambda-functions/stock-ml-get-rsi/package.zip"
  function_name = "stock-ml-get-rsi"
  role          = aws_iam_role.stock-ml.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 60
  runtime = "python3.8"
  memory_size = "128"

  environment {
    variables = sensitive(jsondecode(data.aws_s3_object.env-var.body))
  }

  layers = [
    local.layer-stock-ml
    , data.terraform_remote_state.lambda-layers.outputs.pandas-id
    , data.terraform_remote_state.lambda-layers.outputs.requests-id
  ]
}

resource "aws_lambda_function" "stock-ml-get-macd" {
  s3_bucket     = "do-terraform-1"
  s3_key        = "applications/stock-ml/lambda-functions/stock-ml-get-macd/package.zip"
  function_name = "stock-ml-get-macd"
  role          = aws_iam_role.stock-ml.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 60
  runtime = "python3.8"
  memory_size = "128"

  environment {
    variables = sensitive(jsondecode(data.aws_s3_object.env-var.body))
  }

  layers = [
    local.layer-stock-ml
    , data.terraform_remote_state.lambda-layers.outputs.pandas-id
    , data.terraform_remote_state.lambda-layers.outputs.requests-id
  ]
}

resource "aws_lambda_function" "stock-ml-map-state" {
  s3_bucket     = "do-terraform-1"
  s3_key        = "applications/stock-ml/lambda-functions/stock-ml-map-state/package.zip"
  function_name = "stock-ml-map-state"
  role          = aws_iam_role.stock-ml.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 900
  runtime = "python3.8"
  memory_size = "128"

  layers = [
  ]
}

resource "aws_lambda_function" "stock-ml-invoke-multiple-lambdas" {
  s3_bucket     = "do-terraform-1"
  s3_key        = "applications/stock-ml/lambda-functions/stock-ml-invoke-multiple-lambdas/package.zip"
  function_name = "stock-ml-invoke-multiple-lambdas"
  role          = aws_iam_role.stock-ml.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 600
  runtime = "python3.8"
  memory_size = "128"

  layers = [
  ]
}

resource "aws_lambda_function" "stock-ml-polygon-fact-table" {
  s3_bucket     = "do-terraform-1"
  s3_key        = "applications/stock-ml/lambda-functions/stock-ml-polygon-fact-table/package.zip"
  function_name = "stock-ml-polygon-fact-table"
  role          = aws_iam_role.stock-ml.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 90
  runtime = "python3.8"
  memory_size = "256"

  layers = [
    local.layer-stock-ml
    , data.terraform_remote_state.lambda-layers.outputs.awswrangler-id
  ]
}

resource "aws_lambda_function" "stock-ml-polygon-fact-table-incremental" {
  s3_bucket     = "do-terraform-1"
  s3_key        = "applications/stock-ml/lambda-functions/stock-ml-polygon-fact-table-incremental/package.zip"
  function_name = "stock-ml-polygon-fact-table-incremental"
  role          = aws_iam_role.stock-ml.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 90
  runtime = "python3.8"
  memory_size = "256"

  layers = [
    local.layer-stock-ml
    , data.terraform_remote_state.lambda-layers.outputs.pandas-id
  ]
}

resource "aws_lambda_function" "stock-ml-drop-duplicates" {
  s3_bucket     = "do-terraform-1"
  s3_key        = "applications/stock-ml/lambda-functions/stock-ml-drop-duplicates/package.zip"
  function_name = "stock-ml-drop-duplicates"
  role          = aws_iam_role.stock-ml.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 90
  runtime = "python3.8"
  memory_size = "256"

  layers = [
    data.terraform_remote_state.lambda-layers.outputs.awswrangler-id
  ]
}
