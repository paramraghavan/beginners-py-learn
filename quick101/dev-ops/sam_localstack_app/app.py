import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3', endpoint_url='http://localhost:4566')  # LocalStack S3 endpoint
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    obj = s3.get_object(Bucket=bucket, Key=key)
    content = obj['Body'].read().decode('utf-8')
    print(f"Read file {key} from bucket {bucket}, content:\n{content}")
    return {"statusCode": 200}
