Creating a CI/CD pipeline for a Python backend that interacts with a database, AWS S3, and AWS Lambda, and runs locally
on your laptop for development and testing can be structured as follows:

***

### Real-Life Example Use Case

Imagine building a **Python Lambda function** that processes files uploaded to an AWS S3 bucket, stores metadata into an
AWS RDS database (e.g., PostgreSQL), and runs all automated deployment and testing locally before pushing to AWS.

***

### Components

- **Python Lambda function code** (serverless backend, no Flask)
- **Database access** (AWS RDS or a local PostgreSQL instance for local development)
- **S3 interactions** (mocked or real depending on environment)
- **CI/CD pipeline** managing build, test, deploy steps on local and AWS
- **Local testing** using Docker or AWS SAM CLI to emulate Lambda

***

### Step 1: Python Lambda Function (simplified)

```python
import boto3
import psycopg2
import os

s3 = boto3.client('s3')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'mydb')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')


def lambda_handler(event, context):
    # Extract bucket name and key from event (S3 Put event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Download file from S3 (optional example)
    response = s3.get_object(Bucket=bucket, Key=key)
    file_content = response['Body'].read()

    # Store metadata to database (e.g., file name and size)
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    cur.execute("INSERT INTO files_metadata (file_name, file_size) VALUES (%s, %s)", (key, len(file_content)))
    conn.commit()
    cur.close()
    conn.close()

    return {
        'statusCode': 200,
        'body': f"Processed {key} from {bucket} with size {len(file_content)} bytes"
    }
```

***

### Step 2: Local Development Environment

1. **Database:** Run PostgreSQL locally using Docker for tests:

    ```bash
    docker run --name local-postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=mydb -p 5432:5432 -d postgres
    ```

2. **Mock AWS services:** Use [LocalStack](https://localstack.cloud/) or AWS SAM to emulate S3 and Lambda locally.

3. **Dependencies:** Use a `requirements.txt` including `boto3`, `psycopg2-binary`.

***

### Step 3: Automated Tests Example (`test_lambda.py`)

```python
import unittest
from unittest.mock import patch, MagicMock
import lambda_function  # your lambda function filename without .py


class TestLambdaFunction(unittest.TestCase):

    @patch('lambda_function.boto3.client')
    @patch('lambda_function.psycopg2.connect')
    def test_lambda_handler(self, mock_connect, mock_boto_client):
        # Mock S3 client and get_object response
        mock_s3_client = MagicMock()
        mock_s3_client.get_object.return_value = {'Body': MagicMock(read=lambda: b'file content')}
        mock_boto_client.return_value = mock_s3_client

        # Mock database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simulated event input
        event = {
            'Records': [{
                's3': {
                    'bucket': {'name': 'my-test-bucket'},
                    'object': {'key': 'test-file.txt'}
                }
            }]
        }

        response = lambda_function.lambda_handler(event, None)

        # Validate database insert call
        mock_cursor.execute.assert_called_with("INSERT INTO files_metadata (file_name, file_size) VALUES (%s, %s)",
                                               ('test-file.txt', len(b'file content')))

        # Validate response
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('test-file.txt', response['body'])


if __name__ == '__main__':
    unittest.main()
```

***

### Step 4: CI/CD Pipeline Workflow (Local + AWS)

- **Build & Test Locally:**

    - Run tests locally (`python -m unittest`).
    - Use Docker compose or scripts to spin up PostgreSQL and LocalStack for integration tests.

- **Deploy:**

    - Package Lambda function (including dependencies) with AWS SAM CLI or AWS CLI.
    - Deploy Lambda function and infrastructure (S3 bucket, RDS instance) to AWS.

- **Pipeline Automation Scripts:**

Example shell commands or Python scripts to:

```bash
# Run unit tests locally
python -m unittest discover

# Package lambda
sam build

# Deploy lambda to AWS
sam deploy --stack-name my-lambda-stack --capabilities CAPABILITY_IAM
```

***

### Tools You Can Use Locally for this Pipeline

- **AWS SAM CLI**: Local Lambda and API Gateway emulation, packaging, deployment.
- **LocalStack**: Local AWS service emulation (S3, Lambda, RDS).
- **Docker**: For running PostgreSQL locally.
- **GitHub Actions / Jenkins / other CI**: To automate the above scripts for build, test, deployment on push.

***

### Summary

This pipeline combines Python backend code (AWS Lambda), AWS services (S3, RDS), and database interaction tested fully
locally using Docker and service emulators before deploying to AWS via automated CI/CD commands. It demonstrates a
real-world DevOps workflow with cloud-based infrastructure while accommodating local development efficiently.

