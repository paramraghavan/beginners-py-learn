AWS SAM (Serverless Application Model) and LocalStack are popular tools to develop, test, and deploy serverless applications locally and on AWS.

***

### AWS SAM (Serverless Application Model)

AWS SAM is an open-source framework that simplifies building serverless applications using AWS Lambda, API Gateway, DynamoDB, and more. It extends AWS CloudFormation for defining serverless resources with a concise syntax.

- **Features:**
  - Define Lambda functions, APIs, databases, and event sources in a SAM template.
  - Local build, test, and debug of Lambda functions with SAM CLI.
  - Package and deploy serverless applications to AWS easily.

**Example SAM Template (`template.yaml`):**

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: python3.10
      Handler: app.lambda_handler
      CodeUri: .
      Events:
        S3Event:
          Type: S3
          Properties:
            Bucket: my-bucket
            Events: s3:ObjectCreated:*
```

**Basic Commands:**

- `sam build` — builds the application locally.
- `sam local invoke` — invoke Lambda function locally.
- `sam local start-api` — emulate API Gateway locally.
- `sam deploy` — deploy app to AWS.

***

### LocalStack

LocalStack is a fully functional local AWS cloud stack emulator that lets you develop and test cloud apps offline. It simulates AWS services like Lambda, S3, DynamoDB, etc., locally.

- **Use cases:**
  - Test AWS service interactions without using real AWS account or incurring cost.
  - Integrate with CI pipelines to run integration tests against local AWS services.

**Running LocalStack with Docker:**

```bash
docker run --rm -it -p 4566:4566 -p 4571:4571 localstack/localstack
```

**Access AWS services locally at:**

- Endpoint URL: `http://localhost:4566`

***

### Python Example Using SAM & LocalStack

**`requirements.txt`**

```
boto3
psycopg2-binary
aws-lambda-powertools  # for Lambda utilities (optional)
```

**Python Lambda (`app.py`):**

```python
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3', endpoint_url='http://localhost:4566')  # LocalStack S3 endpoint
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    print(f"Processed file {key} from bucket {bucket} with content: {content}")
    return {'statusCode': 200}
```

***

### Summary

- **AWS SAM**: Helps define, build, test, and deploy serverless AWS apps locally and on cloud with simplified CloudFormation.
- **LocalStack**: Provides simulated AWS services locally so you can develop and test offline.
- **Typical Python modules**: `boto3` to interact with AWS services, `psycopg2-binary` for Postgres if needed, plus Lambda utils like `aws-lambda-powertools`.

Together, SAM and LocalStack enable fast, cost-effective serverless development and CI/CD pipelines by emulating AWS environment on your laptop.

