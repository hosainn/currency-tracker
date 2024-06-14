variable "table_name" {
  description = "Name of the DynamoDB table to store currency"
  default     = "currency-history"
}

variable "read_capacity" {
  description = "Read capacity units (RCUs)"
  default     = 5
}

variable "write_capacity" {
  description = "Write capacity units (WCUs)"
  default     = 5
}

variable "exchange_rate_fetcher_scedule" {
  description = "Schedle to fetch exchange rate"
  default     = "rate(1 minute)"
}
