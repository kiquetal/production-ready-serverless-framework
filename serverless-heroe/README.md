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
`
