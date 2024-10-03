resource "aws_iam_role" "stock-ml" {
  name = "stock-ml"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": ["lambda.amazonaws.com", "states.amazonaws.com"]
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
  
 inline_policy {
    name   = "stock-ml"
    policy = data.aws_iam_policy_document.stock-ml.json
  }
  
  
  inline_policy {
    name   = "log-group"
    policy = data.aws_iam_policy_document.log-group.json
  }
}

data "aws_iam_policy_document" "stock-ml" {
  statement {
    actions   = ["s3:*"]
    resources = [
                "arn:aws:s3:::stock-ml-1/*",
                "arn:aws:s3:::stock-ml-1"
            ]
  }
  
  statement {
    actions   = ["lambda:InvokeFunction"]
    resources = [
                "arn:aws:lambda:us-east-2:913902556403:function:stock-ml-*"
            ]
  }
  
  statement {
    actions   = ["states:StartExecution"]
    resources = [
                "arn:aws:states:us-east-2:913902556403:stateMachine:stock-ml-*"
            ]
  }
}

data "aws_iam_policy_document" "log-group" {
  statement {
    actions   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
    resources = [
                "arn:aws:logs:us-east-2:913902556403:*"
            ]
  }
}
