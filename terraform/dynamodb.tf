resource "aws_dynamodb_table" "currency_history_table" {
  name         = var.table_name
  hash_key     = "date"
  billing_mode = "PROVISIONED"

  attribute {
    name = "date"
    type = "S"
  }

  read_capacity  = var.read_capacity
  write_capacity = var.write_capacity
}
