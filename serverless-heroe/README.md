<!--
title: 'Serverless-Heroe Course Repository'
description: 'This repository is used to follow the serverless-heroe course offered by Yan Cui.'
layout: Doc
framework: v4
platform: AWS
language: python
-->

# Serverless-Heroe Course Repository

This repository is used to follow the "serverless-heroe" course offered by Yan Cui. It demonstrates how to create serverless applications using the Serverless Framework v4 with Python running on AWS Lambda and API Gateway.

The current implementation includes a simple HTTP API that lists all S3 buckets in your AWS account, demonstrating basic AWS service integration.

## Table of Contents
- [Usage](#usage)
  - [Deployment](#deployment)
  - [Invocation](#invocation)
  - [Local development](#local-development)
- [Lambda Layers and Dependencies](#lambda-layers-and-dependencies)
- [GitHub Actions with AWS OIDC Authentication](#github-actions-with-aws-oidc-authentication)

## API Endpoints

### 1. Index Page

- **URL**: `/`
- **Method**: GET
- **Description**: Returns a static HTML page with the restaurant application.
- **Handler**: `lambdas/index.load_restaurants`
- **Authentication**: None (publicly accessible)
- **CORS**: Enabled

### 2. Get Restaurants

- **URL**: `/restaurants`
- **Method**: GET
- **Description**: Returns a list of restaurants from DynamoDB.
- **Handler**: `lambdas/restaurants.handler`
- **Authentication**: AWS IAM (requires SigV4 signed requests)
- **CORS**: Enabled
- **Environment Variables**:
  - `RESTAURANTS_TABLE`: DynamoDB table name for restaurants
  - `default_results`: 8 (default number of results)

### 3. Search Restaurants

- **URL**: `/restaurants/search`
- **Method**: POST
- **Description**: Searches for restaurants based on provided criteria.
- **Handler**: `lambdas/search-restaurants.handler`
- **Authentication**: Cognito User Pools
- **Environment Variables**:
  - `RESTAURANTS_TABLE`: DynamoDB table name for restaurants
  - `default_results`: 8 (default number of results)

You can deploy the service using the following command:

```
serverless deploy
```

This will deploy using the default stage ('dev') and the default AWS profile.

To specify a different stage or AWS profile, you can use the `--stage` and `--aws-profile` parameters:

```
serverless deploy --stage prod --aws-profile production
```

This will deploy to the 'prod' stage using the 'production' AWS profile.

After deploying, you should see output similar to:

```
Deploying "aws-python-http-api" to stage "dev" (us-east-1)

✔ Service deployed to stack aws-python-http-api-dev (85s)

endpoint: GET - https://6ewcye3q4d.execute-api.us-east-1.amazonaws.com/
functions:
  hello: aws-python-http-api-dev-hello (2.3 kB)
```

### Invocation

After successful deployment, you can call the created application via HTTP:

```
curl https://xxxxxxx.execute-api.us-east-1.amazonaws.com/
```

Which should result in response similar to the following:

```json
{
  "message": "Go Serverless v4.0! Your function executed successfully!",
  "buckets": ["bucket1", "bucket2", "bucket3"]
}
```

The `buckets` array will contain the names of all S3 buckets in your AWS account.

### Local development

You can invoke your function locally by using the following command:

```
serverless invoke local --function hello
```

**Important**: When using `serverless invoke local`, use the function name as defined in your `serverless.yml` file, not the handler function name from your code. For example, if your serverless.yml defines a function named `listBuckets` that uses the handler `lambdas/handler.getBuckets`, you would use:

```
serverless invoke local --function listBuckets
```

You can also specify a stage and profile for local invocation:

```
serverless invoke local --function hello --stage prod --aws-profile production
```

## Project Structure
- `lambdas/`: Contains Lambda function handlers
- `lib/`: Contains shared utility functions
- `static/`: Contains static HTML files served by the application

## Seeding Test Data Locally

To seed the DynamoDB table with test data locally (using LocalStack), you can use the following command:

```bash
python seed_data.py --table YOUR_TABLE_NAME [options]
```

Available options:
- `--table`: (Required) The name of the DynamoDB table
- `--endpoint-url`: LocalStack endpoint URL (default: http://localhost:4566)
- `--profile`: AWS profile to use
- `--create-table`: Create the table before seeding data

Example usage:
```bash
# Seed data into existing table
python seed_data.py --table restaurants

# Create table and seed data
python seed_data.py --table restaurants --create-table

# Use custom endpoint and profile
python seed_data.py --table restaurants --endpoint-url http://localhost:4566 --profile localstack
```

### Using with Real AWS (Production)

To seed data into a real AWS DynamoDB table, simply omit the `--endpoint-url` parameter:

```bash
# Seed data into existing AWS DynamoDB table
python seed-restaurants.py --table my-production-table

python seed_data.py --table restaurants --endpoint-url None --profile localstack

## Lambda Layers and Dependencies

This project uses the `serverless-python-requirements` plugin to automatically handle Python dependencies and create Lambda layers. Here's how it works:

### Plugin Configuration

The plugin is configured in `serverless.yml`:

```yaml
plugins:
  - serverless-python-requirements

custom:
  pythonRequirements:
    layer: true
    noDeploy:
      - pytest
      - boto3
      - botocore
    dockerizePip: true
```

### How It Works

1. The plugin reads your `requirements.txt` file
2. When `layer: true` is set, it:
   - Creates a Lambda layer containing all dependencies
   - Packages dependencies into a ZIP file
   - Uploads the layer to AWS
   - Automatically attaches the layer to your functions

3. The `dockerizePip: true` option:
   - Builds dependencies in a Docker container
   - Ensures compatibility with Lambda's runtime environment
   - Handles platform-specific packages correctly

4. The `noDeploy` list excludes packages that:
   - Are already provided by AWS Lambda
   - Are only needed for development

### Working with Layers

To update dependencies:

1. Modify your `requirements.txt`
2. Run `serverless deploy`
3. The plugin will:
   - Rebuild the layer with new dependencies
   - Create a new layer version
   - Update your functions to use the new layer

The layers are managed automatically, so you don't need to handle them manually.

## GitHub Actions with AWS OIDC Authentication

This section explains how to configure GitHub Actions to authenticate with AWS using OpenID Connect (OIDC), allowing your workflows to assume IAM roles without storing AWS credentials as GitHub secrets.

### Overview

Using OIDC for GitHub Actions with AWS provides several benefits:
- No long-lived AWS credentials stored in GitHub
- Temporary, automatically rotated credentials
- Fine-grained access control using IAM roles
- Improved security posture

### Step 1: Create an OIDC Identity Provider in AWS

1. Sign in to the AWS Management Console
2. Navigate to IAM > Identity providers > Add provider
3. Select "OpenID Connect" as the provider type
4. For Provider URL, enter: `https://token.actions.githubusercontent.com`
5. For Audience, enter: `sts.amazonaws.com`
6. Click "Get thumbprint" to retrieve the certificate thumbprint
7. Click "Add provider" to create the OIDC provider

### Step 2: Create an IAM Role for GitHub Actions

1. Go to IAM > Roles > Create role
2. Select "Web identity" as the trusted entity type
3. Choose the GitHub OIDC provider you just created
4. For Audience, select `sts.amazonaws.com`
5. Add a condition to specify which GitHub repositories can use this role:

```json
{
  "StringLike": {
    "token.actions.githubusercontent.com:sub": "repo:your-org/your-repo:*"
  }
}
```

6. Click "Next" and attach the permissions policies this role needs (e.g., `AmazonS3ReadOnlyAccess`)
7. Give the role a name (e.g., `GitHubActionsRole`)
8. Complete the role creation process

### Step 3: Configure GitHub Actions Workflow

Create or update your GitHub Actions workflow file (e.g., `.github/workflows/deploy.yml`):

```yaml
name: Deploy to AWS

on:
  push:
    branches: [ main ]

permissions:
  id-token: write   # Required for OIDC authentication
  contents: read    # Required to checkout repository

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
          aws-region: us-east-1

      - name: Deploy with Serverless Framework
        run: |
          npm install -g serverless
          serverless deploy
```

### Step 4: Fine-tuning Access Control (Optional)

For better security, you can add additional conditions to the IAM role's trust policy:

- Restrict to specific branches:
  ```json
  "StringEquals": {
    "token.actions.githubusercontent.com:sub": "repo:your-org/your-repo:ref:refs/heads/main"
  }
  ```

- Restrict to specific environments:
  ```json
  "StringEquals": {
    "token.actions.githubusercontent.com:sub": "repo:your-org/your-repo:environment:production"
  }
  ```

### Troubleshooting

If you encounter authentication issues:

1. Verify the GitHub workflow has the proper `permissions` block
2. Check the IAM role trust policy for correct repository format
3. Ensure the role has the necessary permissions
4. Confirm the AWS region is correctly specified in the workflow

### Security Best Practices

- Scope IAM permissions to the minimum required for your workflows
- Use branch and environment restrictions for sensitive operations
- Regularly audit and rotate any long-lived credentials
- Consider setting up boundary permissions for GitHub Actions roles

For more information, refer to the [GitHub OIDC documentation](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services) and [AWS IAM documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html).

