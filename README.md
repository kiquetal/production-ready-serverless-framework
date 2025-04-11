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

## Usage

### Deployment

```
serverless deploy
```

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

This will display the resolved configuration after variables substitution, which can help identify any issues with your `serverless.yml` file.

To test the S3 bucket listing functionality without deploying, you can run:

```
serverless invoke local --function hello
```

If everything is set up correctly, you should see a response with your S3 buckets listed in the output.
