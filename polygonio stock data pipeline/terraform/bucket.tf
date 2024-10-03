resource "aws_s3_bucket" "stock-ml" {
  bucket = "stock-ml-1"

}

resource "aws_s3_bucket_acl" "stock-ml-acl" {
  bucket = aws_s3_bucket.stock-ml.id
  acl    = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "stock-ml-sec" {
  bucket = aws_s3_bucket.stock-ml.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "AES256"
    }
  }
}
