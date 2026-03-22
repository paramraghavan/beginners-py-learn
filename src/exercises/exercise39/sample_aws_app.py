"""
Sample AWS application that uses multiple services via boto3.
This is used to demonstrate permission requirements analysis.
"""

import boto3
import json
from datetime import datetime


class AWSResourceManager:
    """Manages various AWS resources."""

    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.ec2_client = boto3.client('ec2')
        self.dynamodb = boto3.resource('dynamodb')
        self.sns_client = boto3.client('sns')
        self.iam_client = boto3.client('iam')
        self.lambda_client = boto3.client('lambda')
        self.eks_client = boto3.client('eks')
        self.emr_client = boto3.client('emr')
        self.es_client = boto3.client('es')

    # ============ S3 Operations ============
    def list_buckets(self):
        """List all S3 buckets - requires s3:ListAllMyBuckets"""
        response = self.s3_client.list_buckets()
        return response['Buckets']

    def upload_file(self, bucket, key, data):
        """Upload file to S3 - requires s3:PutObject"""
        self.s3_client.put_object(Bucket=bucket, Key=key, Body=data)

    def download_file(self, bucket, key):
        """Download file from S3 - requires s3:GetObject"""
        response = self.s3_client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read()

    def delete_file(self, bucket, key):
        """Delete file from S3 - requires s3:DeleteObject"""
        self.s3_client.delete_object(Bucket=bucket, Key=key)

    def list_objects(self, bucket, prefix):
        """List objects in bucket - requires s3:ListBucket"""
        response = self.s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        return response.get('Contents', [])

    # ============ EC2 Operations ============
    def list_instances(self):
        """List EC2 instances - requires ec2:DescribeInstances"""
        response = self.ec2_client.describe_instances()
        return response['Reservations']

    def start_instance(self, instance_id):
        """Start EC2 instance - requires ec2:StartInstances"""
        self.ec2_client.start_instances(InstanceIds=[instance_id])

    def stop_instance(self, instance_id):
        """Stop EC2 instance - requires ec2:StopInstances"""
        self.ec2_client.stop_instances(InstanceIds=[instance_id])

    def create_security_group(self, group_name, description, vpc_id):
        """Create security group - requires ec2:CreateSecurityGroup"""
        response = self.ec2_client.create_security_group(
            GroupName=group_name,
            Description=description,
            VpcId=vpc_id
        )
        return response['GroupId']

    # ============ DynamoDB Operations ============
    def create_table(self, table_name):
        """Create DynamoDB table - requires dynamodb:CreateTable"""
        table = self.dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        return table

    def put_item(self, table_name, item):
        """Put item in DynamoDB - requires dynamodb:PutItem"""
        table = self.dynamodb.Table(table_name)
        table.put_item(Item=item)

    def get_item(self, table_name, key):
        """Get item from DynamoDB - requires dynamodb:GetItem"""
        table = self.dynamodb.Table(table_name)
        response = table.get_item(Key=key)
        return response.get('Item')

    def scan_table(self, table_name):
        """Scan DynamoDB table - requires dynamodb:Scan"""
        table = self.dynamodb.Table(table_name)
        response = table.scan()
        return response['Items']

    # ============ SNS Operations ============
    def create_topic(self, topic_name):
        """Create SNS topic - requires sns:CreateTopic"""
        response = self.sns_client.create_topic(Name=topic_name)
        return response['TopicArn']

    def publish_message(self, topic_arn, message):
        """Publish to SNS topic - requires sns:Publish"""
        self.sns_client.publish(TopicArn=topic_arn, Message=message)

    # ============ IAM Operations ============
    def list_users(self):
        """List IAM users - requires iam:ListUsers"""
        response = self.iam_client.list_users()
        return response['Users']

    def get_user_info(self, username):
        """Get user info - requires iam:GetUser"""
        response = self.iam_client.get_user(UserName=username)
        return response['User']

    def list_roles(self):
        """List IAM roles - requires iam:ListRoles"""
        response = self.iam_client.list_roles()
        return response['Roles']

    # ============ Lambda Operations ============
    def list_functions(self):
        """List Lambda functions - requires lambda:ListFunctions"""
        response = self.lambda_client.list_functions()
        return response['Functions']

    def create_lambda_function(self, function_name, runtime, role, handler, zip_file):
        """Create Lambda function - requires lambda:CreateFunction"""
        response = self.lambda_client.create_function(
            FunctionName=function_name,
            Runtime=runtime,
            Role=role,
            Handler=handler,
            Code={'ZipFile': zip_file}
        )
        return response

    def invoke_lambda(self, function_name, payload):
        """Invoke Lambda function - requires lambda:InvokeFunction"""
        response = self.lambda_client.invoke(
            FunctionName=function_name,
            Payload=json.dumps(payload)
        )
        return response

    def delete_lambda_function(self, function_name):
        """Delete Lambda function - requires lambda:DeleteFunction"""
        self.lambda_client.delete_function(FunctionName=function_name)

    def update_lambda_code(self, function_name, zip_file):
        """Update Lambda function code - requires lambda:UpdateFunctionCode"""
        response = self.lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_file
        )
        return response

    # ============ EKS Operations ============
    def list_eks_clusters(self):
        """List EKS clusters - requires eks:ListClusters"""
        response = self.eks_client.list_clusters()
        return response['clusters']

    def describe_eks_cluster(self, cluster_name):
        """Describe EKS cluster - requires eks:DescribeCluster"""
        response = self.eks_client.describe_cluster(name=cluster_name)
        return response['cluster']

    def create_eks_cluster(self, cluster_name, version, role_arn, subnet_ids):
        """Create EKS cluster - requires eks:CreateCluster"""
        response = self.eks_client.create_cluster(
            name=cluster_name,
            version=version,
            roleArn=role_arn,
            resourcesVpcConfig={'subnetIds': subnet_ids}
        )
        return response

    def delete_eks_cluster(self, cluster_name):
        """Delete EKS cluster - requires eks:DeleteCluster"""
        response = self.eks_client.delete_cluster(name=cluster_name)
        return response

    def list_eks_nodegroups(self, cluster_name):
        """List EKS nodegroups - requires eks:ListNodegroups"""
        response = self.eks_client.list_nodegroups(clusterName=cluster_name)
        return response['nodegroups']

    # ============ EMR Operations ============
    def list_emr_clusters(self):
        """List EMR clusters - requires elasticmapreduce:ListClusters"""
        response = self.emr_client.list_clusters()
        return response['Clusters']

    def describe_emr_cluster(self, cluster_id):
        """Describe EMR cluster - requires elasticmapreduce:DescribeCluster"""
        response = self.emr_client.describe_cluster(ClusterId=cluster_id)
        return response['Cluster']

    def run_emr_cluster(self, name, release_label, instances, applications):
        """Create/run EMR cluster - requires elasticmapreduce:RunJobFlow"""
        response = self.emr_client.run_job_flow(
            Name=name,
            ReleaseLabel=release_label,
            Instances=instances,
            Applications=applications
        )
        return response

    def add_emr_steps(self, cluster_id, steps):
        """Add steps to EMR cluster - requires elasticmapreduce:AddJobFlowSteps"""
        response = self.emr_client.add_job_flow_steps(
            JobFlowId=cluster_id,
            Steps=steps
        )
        return response

    def terminate_emr_cluster(self, cluster_id):
        """Terminate EMR cluster - requires elasticmapreduce:TerminateJobFlows"""
        response = self.emr_client.terminate_job_flows(JobFlowIds=[cluster_id])
        return response

    # ============ Elasticsearch Operations ============
    def list_es_domains(self):
        """List Elasticsearch domains - requires es:ListDomainNames"""
        response = self.es_client.list_domain_names()
        return response['DomainNames']

    def describe_es_domain(self, domain_name):
        """Describe Elasticsearch domain - requires es:DescribeElasticsearchDomain"""
        response = self.es_client.describe_elasticsearch_domain(DomainName=domain_name)
        return response['DomainStatus']

    def create_es_domain(self, domain_name, elasticsearch_version):
        """Create Elasticsearch domain - requires es:CreateElasticsearchDomain"""
        response = self.es_client.create_elasticsearch_domain(
            DomainName=domain_name,
            ElasticsearchVersion=elasticsearch_version
        )
        return response

    def delete_es_domain(self, domain_name):
        """Delete Elasticsearch domain - requires es:DeleteElasticsearchDomain"""
        response = self.es_client.delete_elasticsearch_domain(DomainName=domain_name)
        return response

    def update_es_domain_config(self, domain_name, config):
        """Update Elasticsearch domain - requires es:UpdateElasticsearchDomainConfig"""
        response = self.es_client.update_elasticsearch_domain_config(
            DomainName=domain_name,
            ElasticsearchClusterConfig=config
        )
        return response


def main():
    """Example usage of AWSResourceManager."""
    manager = AWSResourceManager()

    # List buckets
    try:
        buckets = manager.list_buckets()
        print(f"Found {len(buckets)} buckets")
    except Exception as e:
        print(f"Error listing buckets: {e}")

    # List instances
    try:
        instances = manager.list_instances()
        print(f"Found instances: {instances}")
    except Exception as e:
        print(f"Error listing instances: {e}")

    # List users
    try:
        users = manager.list_users()
        print(f"Found {len(users)} users")
    except Exception as e:
        print(f"Error listing users: {e}")

    # List Lambda functions
    try:
        functions = manager.list_functions()
        print(f"Found {len(functions)} Lambda functions")
    except Exception as e:
        print(f"Error listing Lambda functions: {e}")

    # List EKS clusters
    try:
        clusters = manager.list_eks_clusters()
        print(f"Found {len(clusters)} EKS clusters")
    except Exception as e:
        print(f"Error listing EKS clusters: {e}")

    # List EMR clusters
    try:
        emr_clusters = manager.list_emr_clusters()
        print(f"Found {len(emr_clusters)} EMR clusters")
    except Exception as e:
        print(f"Error listing EMR clusters: {e}")

    # List Elasticsearch domains
    try:
        es_domains = manager.list_es_domains()
        print(f"Found {len(es_domains)} Elasticsearch domains")
    except Exception as e:
        print(f"Error listing Elasticsearch domains: {e}")


if __name__ == '__main__':
    main()
