# Currency Tracker Terraform Deployment

## Overview

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

Replace the placeholders with your actual AWS credentials and preferred region.

Deployment Steps
Step 1: Navigate to the Terraform Directory
Navigate to the currency-tracker/terraform/ directory:

bash
Copy code
cd currency-tracker/terraform/
Step 2: Initialize Terraform
Run the following command to initialize Terraform. This will download the necessary provider plugins and prepare your environment for deployment.

bash
Copy code
terraform init
Step 3: Apply Terraform Configuration
Deploy the infrastructure by running the apply command with the -auto-approve flag to bypass manual approval.

bash
Copy code
terraform apply -auto-approve
Step 4: Verify Deployment
Check the AWS Management Console to verify that the infrastructure has been deployed correctly. Ensure all the necessary resources are created and configured as expected.

Step 5: Destroy Terraform Resources
If you need to tear down the infrastructure, use the destroy command with the -auto-approve flag.

bash
Copy code
terraform destroy -auto-approve
Notes
Ensure that your AWS credentials have the necessary permissions to create and destroy resources.
Review the Terraform configurations and variables to understand what resources will be created.
Be cautious when using the -auto-approve flag in a production environment, as it will automatically approve changes without manual confirmation.
By following these steps, you can easily manage the infrastructure for the Currency Tracker application using Terraform.