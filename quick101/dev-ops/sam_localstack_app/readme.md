Here is a step-by-step minimal example project demonstrating AWS SAM and LocalStack integration for a Python Lambda
function with S3 event trigger, including how to test locally on your laptop.

***

### Project Structure

```
my-sam-app/
│
├── app.py           # Lambda Python function
├── requirements.txt # Python dependencies
├── template.yaml    # SAM template
└── README.md
```

***

### `app.py`

```python
import boto3


def lambda_handler(event, context):
    s3 = boto3.client('s3', endpoint_url='http://localhost:4566')  # LocalStack S3 endpoint
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    obj = s3.get_object(Bucket=bucket, Key=key)
    content = obj['Body'].read().decode('utf-8')
    print(f"Read file {key} from bucket {bucket}, content:\n{content}")
    return {"statusCode": 200}
```

***

### `requirements.txt`

```
boto3
```

***

### `template.yaml` (SAM template)

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  MyLambdaFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: .
      Handler: app.lambda_handler
      Runtime: python3.10
      Events:
        S3Event:
          Type: S3
          Properties:
            Bucket: my-test-bucket
            Events: s3:ObjectCreated:*
```

***

### Steps to Run Locally with SAM and LocalStack

1. **Install prerequisites:**

- AWS SAM CLI
- Docker
- LocalStack (run via Docker: `docker run -d -p 4566:4566 -p 4571:4571 localstack/localstack`)

2. **Create the S3 bucket in LocalStack:**

```bash
aws --endpoint-url=http://localhost:4566 s3 mb s3://my-test-bucket
```

3. **Build your SAM app:**

```bash
sam build
```

4. **Invoke Lambda locally simulating S3 event:**

Create a file `event.json`:

```json
{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "my-test-bucket"
        },
        "object": {
          "key": "test-file.txt"
        }
      }
    }
  ]
}
```

Invoke locally:

```bash
sam local invoke MyLambdaFunction -e event.json --docker-network host
```

5. **Upload a test file to LocalStack S3:**

```bash
aws --endpoint-url=http://localhost:4566 s3 cp test-file.txt s3://my-test-bucket/
```

Replace `test-file.txt` with your test file to see the Lambda read the content.

***

This setup allows full local development, testing, and debugging of AWS Lambda functions triggered by S3 events with
LocalStack emulating AWS services and SAM managing builds and local invocations.

You can include other dependencies in `requirements.txt` as needed and extend to other AWS resources.
