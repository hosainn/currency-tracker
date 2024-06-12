terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.53.0"
    }
  }
}

provider "aws" {
  default_tags {
    tags = {
      Environment = local.environment
    }
  }
}
