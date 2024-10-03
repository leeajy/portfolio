######################################################
# Roles

resource "aws_iam_role" "whale-shark" {
  name = "whale-shark-v2"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
  
 inline_policy {
    name   = "whale-shark"
    policy = data.aws_iam_policy_document.whale-shark.json
  }
}

######################################################
# Policies

data "aws_iam_policy_document" "whale-shark" {
  statement {
    actions   = ["s3:*","lambda:InvokeFunction"]
    resources = [
                "arn:aws:lambda:us-east-2:913902556403:function:whale-shark-*",
                "arn:aws:s3:::whale-shark/*",
                "arn:aws:s3:::whale-shark"
            ]
  }
}
