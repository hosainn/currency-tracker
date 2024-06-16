# Currency Tracker Terraform Deployment

## Project Description

The goal of this project is to design and build a currency exchange tracking application within the AWS Lambda environment. The application will fetch exchange rate data from the [European Central Bank (ECB)](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html) on a daily basis around 16:05 CET and store this information in a database. It will expose a public REST API endpoint that allows clients to retrieve current exchange rates for tracked currencies and understand how these rates have changed compared to the previous day.

## [Click here](https://app.diagrams.net/?mode=google#G1tQ7Svd47gaxt3MSCQu4wSA-HYGgi-P50#%7B%22pageId%22%3A%22DpC3ov5GFhaDNXzQjg_z%22%7D) to see technical design




## Development Overview

This project uses Terraform to manage the infrastructure for the Currency Tracker application. The deployment is designed for an AWS environment and includes steps to initialize, apply, and destroy the Terraform-managed resources.

## Prerequisites

Before starting, ensure the following software is installed:

- Python 3.8 or higher
- Terraform v1.8.5-dev or higher

Additionally, make sure you have the necessary environment variables set up for AWS access:

```bash
export AWS_ACCESS_KEY_ID=<YOUR_AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<YOUR_AWS_SECRET_ACCESS_KEY>
export AWS_DEFAULT_REGION=<YOUR_AWS_DEFAULT_REGION>
```

Replace the placeholders with your actual AWS credentials and preferred region.

### Deployment Steps
#### Step 1: Navigate to the Terraform Directory
Navigate to the currency-tracker/terraform/ directory:

```
cd currency-tracker/terraform/
```

#### Step 2: Initialize Terraform
Run the following command to initialize Terraform. This will download the necessary provider plugins and prepare your environment for deployment.

```
terraform init
```
Step 3: Apply Terraform Configuration
Deploy the infrastructure by running the apply command with the -auto-approve flag to bypass manual approval.

```
terraform apply -auto-approve
```
After successfully executing the command above, retrieve the base URL displayed in the console or terminal. Append /exchange-rates to this base URL to access the API endpoints.

For detailed API documentation, refer to the OpenAPI specification provided at:

```
currency-tracker/docs/openapi.yaml
```

#### Step 4: Verify Deployment

Check the AWS Management Console to verify that the infrastructure has been deployed correctly. Ensure all the necessary resources are created and configured as expected.

### Destroy Terraform Resources
If you need to tear down the infrastructure, use the destroy command with the -auto-approve flag.

```
terraform destroy -auto-approve
```