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
  - [Bundling dependencies](#bundling-dependencies)
- [Serverless Framework v4 Changes and Guidelines](#serverless-framework-v4-changes-and-guidelines)
  - [Key Changes in Serverless Framework v4](#key-changes-in-serverless-framework-v4)
  - [Using Lambda Layers for Python Requirements](#using-lambda-layers-for-python-requirements)
- [API Gateway Authentication with AWS IAM](#api-gateway-authentication-with-aws-iam)
  - [Authentication Flow](#authentication-flow)
  - [Working with Cognito User Pool and Identity Pool](#working-with-cognito-user-pool-and-identity-pool)
  - [Accessing the Protected API](#accessing-the-protected-api)
- [Verifying Serverless Framework v4 Setup](#verifying-serverless-framework-v4-setup)

## Usage

### Deployment

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

_Note_: In current form, after deployment, your API is public and can be invoked by anyone. For production deployments, you might want to configure an authorizer. For details on how to do that, refer to [http event docs](https://www.serverless.com/framework/docs/providers/aws/events/apigateway/).

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

You can also specify a stage and profile for local invocation:

```
serverless invoke local --function hello --stage prod --aws-profile production
```

Which should result in response similar to the following:

```json
{
  "statusCode": 200,
  "body": "{\n  \"message\": \"Go Serverless v4.0! Your function executed successfully!\",\n  \"buckets\": [\"bucket1\", \"bucket2\", \"bucket3\"]}"
}
```

Alternatively, it is also possible to emulate API Gateway and Lambda locally by using `serverless-offline` plugin. In order to do that, execute the following command:

```
serverless plugin install -n serverless-offline
```

It will add the `serverless-offline` plugin to `devDependencies` in `package.json` file as well as will add it to `plugins` in `serverless.yml`.

After installation, you can start local emulation with:

```
serverless offline
```

To learn more about the capabilities of `serverless-offline`, please refer to its [GitHub repository](https://github.com/dherault/serverless-offline).

### Bundling dependencies

In case you would like to include 3rd party dependencies, you will need to use a plugin called `serverless-python-requirements`. You can set it up by running the following command:

```
serverless plugin install -n serverless-python-requirements
```

Running the above will automatically add `serverless-python-requirements` to `plugins` section in your `serverless.yml` file and add it as a `devDependency` to `package.json` file. The `package.json` file will be automatically created if it doesn't exist beforehand. Now you will be able to add your dependencies to `requirements.txt` file (`Pipfile` and `pyproject.toml` is also supported but requires additional configuration) and they will be automatically injected to Lambda package during build process. For more details about the plugin's configuration, please refer to [official documentation](https://github.com/UnitedIncome/serverless-python-requirements).

## Serverless Framework v4 Changes and Guidelines

Serverless Framework v4 introduces several important changes and improvements compared to v3. Understanding these changes is crucial for migrating existing projects or starting new ones.

### Key Changes in Serverless Framework v4

1. **Global Stage Configuration**:
   - In v3, stage was defined at the provider level: `provider.stage`
   - In v4, stage is now a top-level property: `stage: dev`
   - This change allows for more consistent stage handling across the framework
   - In this project, we use variable substitution to allow command-line specification: `stage: ${opt:stage, 'dev'}`

2. **Improved Variables System**:
   - Enhanced variable resolution with better error messages
   - Support for new variable sources and improved performance
   - More predictable variable resolution order

3. **Streamlined Configuration**:
   - Simplified configuration structure
   - Removal of deprecated properties and features
   - More consistent naming conventions

4. **Enhanced Plugin System**:
   - Better plugin lifecycle management
   - Improved hooks and events system
   - More reliable plugin execution order

5. **AWS Provider Updates**:
   - Updated AWS SDK usage
   - Better support for newer AWS services and features
   - Improved IAM role handling

6. **AWS Profile Configuration**:
   - Serverless Framework supports using named AWS profiles for deployment
   - In this project, we use variable substitution to allow command-line specification: `profile: ${opt:aws-profile, 'default'}`
   - This allows you to easily switch between different AWS accounts or environments

### Using Lambda Layers for Python Requirements

Lambda Layers provide a way to separate your application code from its dependencies, resulting in smaller deployment packages and the ability to share dependencies across multiple functions.

#### Configuration in serverless.yml

This project uses the `serverless-python-requirements` plugin to automatically create a Lambda Layer for Python dependencies:

```yaml
custom:
  pythonRequirements:
    layer: true    # Creates a Lambda Layer for dependencies

functions:
  hello:
    handler: handler.hello
    layers:
      - Ref: PythonRequirementsLambdaLayer  # References the auto-generated layer
```

#### Benefits of Using Layers for Requirements

1. **Smaller Function Packages**: Your function code is deployed separately from dependencies, resulting in smaller packages and faster deployments.

2. **Dependency Reuse**: Multiple functions can share the same layer, reducing duplication and overall deployment size.

3. **Easier Dependency Management**: Dependencies can be updated independently from function code.

4. **Improved Cold Start Performance**: In some cases, using layers can improve cold start times.

#### How to Use Layers for Requirements

1. **Install the Plugin**:
   ```
   serverless plugin install -n serverless-python-requirements
   ```

2. **Configure Your serverless.yml**:
   ```yaml
   custom:
     pythonRequirements:
       layer: true

   functions:
     yourFunction:
       handler: path/to/handler.function
       layers:
         - Ref: PythonRequirementsLambdaLayer
   ```

3. **Specify Dependencies**:
   Add your Python dependencies to `requirements.txt`:
   ```
   boto3==1.34.0
   requests==2.31.0
   ```

4. **Deploy**:
   ```
   serverless deploy
   ```

The plugin will automatically:
1. Install the dependencies from requirements.txt
2. Package them into a Lambda Layer
3. Deploy the layer alongside your functions
4. Configure your functions to use the layer

#### Layer Size Limitations

Be aware that AWS Lambda Layers have a size limit of 250MB (unzipped). If your dependencies exceed this limit, you may need to:
1. Split your dependencies across multiple layers
2. Optimize your dependencies to reduce size
3. Package some dependencies directly with your function code

## API Gateway Authentication with AWS IAM

This project uses AWS IAM authentication to secure API Gateway endpoints. The authentication is implemented using Amazon Cognito User Pools and Identity Pools, which enable users to obtain temporary AWS credentials for accessing the API.

### Authentication Flow

1. **User Registration and Authentication**:
   - Users register and authenticate with Cognito User Pool.
   - After successful authentication, users receive JWT tokens.

2. **Obtaining AWS Credentials**:
   - Users exchange their JWT tokens for temporary AWS credentials via Cognito Identity Pool.
   - These AWS credentials have permissions defined by the authenticated role.

3. **Accessing the API**:
   - API requests must be signed with SigV4 using the temporary AWS credentials.
   - API Gateway validates these signatures before allowing access to the endpoints.

### Working with Cognito User Pool and Identity Pool

After deploying your application, you will have the following resources:

- **Cognito User Pool**: Handles user registration, authentication, and management.
- **Cognito User Pool Client**: Client application that users will interact with.
- **Cognito Identity Pool**: Provides temporary AWS credentials to authenticated users.
- **IAM Roles**: Defines what authenticated users can access (in this case, API Gateway endpoints).

#### Creating Users

You can create users in the Cognito User Pool using the AWS CLI or Console:

```bash
# Using AWS CLI
aws cognito-idp sign-up \
  --client-id YOUR_USER_POOL_CLIENT_ID \
  --username user@example.com \
  --password YourSecurePassword123! \
  --user-attributes Name=email,Value=user@example.com \
  --region YOUR_REGION

# Confirm the user (admin only)
aws cognito-idp admin-confirm-sign-up \
  --user-pool-id YOUR_USER_POOL_ID \
  --username user@example.com \
  --region YOUR_REGION
```

#### Understanding IAM Roles vs IAM Users vs Amazon Cognito

There are important distinctions between these concepts:

- **IAM Users**: Long-term credentials for accessing AWS resources, typically for administrative purposes.
- **IAM Roles**: Sets of permissions that can be assumed temporarily by trusted entities.
- **Cognito User Pool**: User directory for web and mobile apps, handling authentication but not authorization.
- **Cognito Identity Pool**: Provides temporary AWS credentials by assuming IAM roles on behalf of authenticated users.

In this setup:
1. Users authenticate via Cognito User Pool (NOT IAM Users)
2. Cognito Identity Pool assigns them the appropriate IAM Role
3. The IAM Role grants permissions to access the API Gateway

This differs from using custom authorizers because AWS_IAM authentication requires requests to be signed with valid AWS credentials using Signature Version 4 (SigV4).

### Accessing the Protected API

To access the protected API, clients need to:

1. **Authenticate with Cognito User Pool**:
   ```javascript
   // Example with AWS Amplify
   const { idToken } = await Auth.signIn(username, password);
   ```

2. **Get AWS Credentials from Cognito Identity Pool**:
   ```javascript
   // Example with AWS Amplify
   const credentials = await Auth.currentCredentials();
   ```

3. **Sign API Requests with SigV4**:
   ```javascript
   // Example with AWS SDK v3
   import { SignatureV4 } from "@aws-sdk/signature-v4";
   import { Sha256 } from "@aws-crypto/sha256-js";
   
   const signer = new SignatureV4({
     credentials,
     region: "YOUR_REGION",
     service: "execute-api",
     sha256: Sha256
   });
   
   const signed = await signer.sign({
     method: "GET",
     hostname: "YOUR_API_ID.execute-api.YOUR_REGION.amazonaws.com",
     path: "/",
     headers: {
       host: "YOUR_API_ID.execute-api.YOUR_REGION.amazonaws.com"
     }
   });
   
   // Now use signed.headers in your fetch request
   ```

#### Using AWS CLI to Test the API

For testing purposes, you can use the AWS CLI with your own AWS credentials:

```bash
aws apigatewayv2 get-api \
  --api-id YOUR_API_ID \
  --region YOUR_REGION
```

Note: The IAM role associated with your CLI credentials must have permission to invoke the API Gateway.

## Verifying Serverless Framework v4 Setup

To check if your Serverless Framework v4 setup is working correctly, you can run the following command:

```
serverless --version
```

This should display the version of the Serverless Framework you're using. Make sure it shows version 4.x.x.

You can also verify that your configuration is correct by running:

```
serverless print
```

To verify your configuration with a specific stage and profile, you can run:

```
serverless print --stage prod --aws-profile production
```

This will display the resolved configuration after variables substitution, which can help identify any issues with your `serverless.yml` file and ensure that the stage and profile parameters are being applied correctly.

To test the S3 bucket listing functionality without deploying, you can run:

```
serverless invoke local --function hello
```

Or with a specific stage and profile:

```
serverless invoke local --function hello --stage prod --aws-profile production
```

If everything is set up correctly, you should see a response with your S3 buckets listed in the output.
`
