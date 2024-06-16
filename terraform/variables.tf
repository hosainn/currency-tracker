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
  default     = "cron(5 15 * * ?)"
}


variable "ecb_exchange_rates_url" {
  description = "URL for fetching daily exchange rates from ECB"
  default     = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
}

variable "ecb_namespace" {
  description = "Namespace for XML elements in ECB exchange rates XML"
  default     = "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"
}
