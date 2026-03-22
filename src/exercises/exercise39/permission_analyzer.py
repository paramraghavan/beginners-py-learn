"""
AWS Permission Analyzer - Analyzes Python code to determine required AWS permissions.

Usage:
    python permission_analyzer.py --code-file sample_aws_app.py
    python permission_analyzer.py --code-file sample_aws_app.py --role-name my-role
"""

import boto3
import json
import re
import argparse
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class AWSPermissionAnalyzer:
    """Analyzes AWS permissions required by Python code and current role permissions."""

    # Mapping of boto3 method calls to required IAM permissions
    BOTO3_METHOD_PERMISSIONS = {
        # S3 operations
        's3.list_buckets': ['s3:ListAllMyBuckets'],
        's3.list_objects': ['s3:ListBucket'],
        's3.list_objects_v2': ['s3:ListBucket'],
        's3.get_object': ['s3:GetObject'],
        's3.put_object': ['s3:PutObject'],
        's3.delete_object': ['s3:DeleteObject'],
        's3.head_object': ['s3:GetObject'],
        's3.copy_object': ['s3:GetObject', 's3:PutObject'],

        # EC2 operations
        'ec2.describe_instances': ['ec2:DescribeInstances'],
        'ec2.start_instances': ['ec2:StartInstances'],
        'ec2.stop_instances': ['ec2:StopInstances'],
        'ec2.terminate_instances': ['ec2:TerminateInstances'],
        'ec2.create_security_group': ['ec2:CreateSecurityGroup'],
        'ec2.delete_security_group': ['ec2:DeleteSecurityGroup'],
        'ec2.authorize_security_group_ingress': ['ec2:AuthorizeSecurityGroupIngress'],
        'ec2.create_instance': ['ec2:RunInstances'],

        # DynamoDB operations
        'dynamodb.create_table': ['dynamodb:CreateTable'],
        'dynamodb.delete_table': ['dynamodb:DeleteTable'],
        'dynamodb.put_item': ['dynamodb:PutItem'],
        'dynamodb.get_item': ['dynamodb:GetItem'],
        'dynamodb.update_item': ['dynamodb:UpdateItem'],
        'dynamodb.delete_item': ['dynamodb:DeleteItem'],
        'dynamodb.scan': ['dynamodb:Scan'],
        'dynamodb.query': ['dynamodb:Query'],

        # SNS operations
        'sns.create_topic': ['sns:CreateTopic'],
        'sns.delete_topic': ['sns:DeleteTopic'],
        'sns.publish': ['sns:Publish'],
        'sns.subscribe': ['sns:Subscribe'],

        # IAM operations
        'iam.list_users': ['iam:ListUsers'],
        'iam.get_user': ['iam:GetUser'],
        'iam.create_user': ['iam:CreateUser'],
        'iam.delete_user': ['iam:DeleteUser'],
        'iam.list_roles': ['iam:ListRoles'],
        'iam.get_role': ['iam:GetRole'],
        'iam.create_role': ['iam:CreateRole'],
        'iam.delete_role': ['iam:DeleteRole'],

        # Lambda operations
        'lambda.create_function': ['lambda:CreateFunction'],
        'lambda.update_function_code': ['lambda:UpdateFunctionCode'],
        'lambda.update_function_configuration': ['lambda:UpdateFunctionConfiguration'],
        'lambda.delete_function': ['lambda:DeleteFunction'],
        'lambda.get_function': ['lambda:GetFunction'],
        'lambda.list_functions': ['lambda:ListFunctions'],
        'lambda.invoke': ['lambda:InvokeFunction'],
        'lambda.add_permission': ['lambda:AddPermission'],
        'lambda.get_policy': ['lambda:GetPolicy'],
        'lambda.list_event_source_mappings': ['lambda:ListEventSourceMappings'],
        'lambda.create_event_source_mapping': ['lambda:CreateEventSourceMapping'],

        # EKS operations
        'eks.create_cluster': ['eks:CreateCluster'],
        'eks.describe_cluster': ['eks:DescribeCluster'],
        'eks.delete_cluster': ['eks:DeleteCluster'],
        'eks.list_clusters': ['eks:ListClusters'],
        'eks.update_cluster_version': ['eks:UpdateClusterVersion'],
        'eks.create_nodegroup': ['eks:CreateNodegroup'],
        'eks.describe_nodegroup': ['eks:DescribeNodegroup'],
        'eks.delete_nodegroup': ['eks:DeleteNodegroup'],
        'eks.list_nodegroups': ['eks:ListNodegroups'],

        # EMR operations
        'emr.create_cluster': ['elasticmapreduce:CreateCluster'],
        'emr.describe_cluster': ['elasticmapreduce:DescribeCluster'],
        'emr.terminate_job_flows': ['elasticmapreduce:TerminateJobFlows'],
        'emr.list_clusters': ['elasticmapreduce:ListClusters'],
        'emr.add_job_flow_steps': ['elasticmapreduce:AddJobFlowSteps'],
        'emr.describe_job_flows': ['elasticmapreduce:DescribeJobFlows'],
        'emr.set_termination_protection': ['elasticmapreduce:SetTerminationProtection'],
        'emr.run_job_flow': ['elasticmapreduce:RunJobFlow'],

        # Elasticsearch operations
        'es.create_elasticsearch_domain': ['es:CreateElasticsearchDomain'],
        'es.delete_elasticsearch_domain': ['es:DeleteElasticsearchDomain'],
        'es.describe_elasticsearch_domain': ['es:DescribeElasticsearchDomain'],
        'es.describe_elasticsearch_domains': ['es:DescribeElasticsearchDomains'],
        'es.list_domain_names': ['es:ListDomainNames'],
        'es.update_elasticsearch_domain_config': ['es:UpdateElasticsearchDomainConfig'],
        'es.describe_elasticsearch_domain_config': ['es:DescribeElasticsearchDomainConfig'],
        'es.get_compatible_elasticsearch_versions': ['es:GetCompatibleElasticsearchVersions'],
    }

    def __init__(self):
        self.sts_client = boto3.client('sts')
        self.iam_client = boto3.client('iam')
        self.current_identity = None
        self.current_role_name = None

    def get_current_identity(self) -> Dict:
        """Get current AWS identity information."""
        try:
            response = self.sts_client.get_caller_identity()
            self.current_identity = response
            print(f"✓ Current Identity:")
            print(f"  - User/Role ARN: {response['Arn']}")
            print(f"  - Account: {response['Account']}")
            print(f"  - User ID: {response['UserId']}")

            # Extract role name from ARN
            arn = response['Arn']
            if 'role' in arn:
                self.current_role_name = arn.split('/')[-1]
            else:
                self.current_role_name = arn.split('/')[-1]

            return response
        except Exception as e:
            print(f"✗ Error getting identity: {e}")
            raise

    def get_role_permissions(self, role_name: str = None) -> Dict[str, List[str]]:
        """Get all permissions for a specific IAM role."""
        if role_name is None:
            role_name = self.current_role_name

        if not role_name:
            print("✗ Could not determine role name")
            return {}

        print(f"\n✓ Fetching permissions for role: {role_name}")
        all_permissions = defaultdict(list)

        try:
            # Get inline policies
            inline_policies = self.iam_client.list_role_policies(RoleName=role_name)
            print(f"  - Found {len(inline_policies['PolicyNames'])} inline policies")

            for policy_name in inline_policies['PolicyNames']:
                policy_doc = self.iam_client.get_role_policy(
                    RoleName=role_name,
                    PolicyName=policy_name
                )
                self._extract_permissions(policy_doc['RolePolicy']['Statement'], all_permissions)

            # Get managed policies
            managed_policies = self.iam_client.list_attached_role_policies(RoleName=role_name)
            print(f"  - Found {len(managed_policies['AttachedPolicies'])} managed policies")

            for policy in managed_policies['AttachedPolicies']:
                policy_arn = policy['PolicyArn']
                policy_version = self.iam_client.get_policy(PolicyArn=policy_arn)
                default_version_id = policy_version['Policy']['DefaultVersionId']

                policy_doc = self.iam_client.get_policy_version(
                    PolicyArn=policy_arn,
                    VersionId=default_version_id
                )
                self._extract_permissions(policy_doc['PolicyVersion']['Document']['Statement'], all_permissions)

        except Exception as e:
            print(f"✗ Error fetching role permissions: {e}")

        return dict(all_permissions)

    def _extract_permissions(self, statements: List[Dict], permissions: Dict[str, List[str]]):
        """Extract permissions from IAM policy statements."""
        for statement in statements:
            if statement.get('Effect') == 'Allow':
                actions = statement.get('Action', [])
                resources = statement.get('Resource', ['*'])

                if isinstance(actions, str):
                    actions = [actions]
                if isinstance(resources, str):
                    resources = [resources]

                for action in actions:
                    for resource in resources:
                        if resource not in permissions:
                            permissions[resource] = []
                        if action not in permissions[resource]:
                            permissions[resource].append(action)

    def analyze_code(self, code_content: str) -> Dict[str, Set[str]]:
        """Analyze Python code to find required AWS permissions."""
        required_permissions = defaultdict(set)

        # Step 1: Build a mapping of variable names to AWS services
        # Track both local and instance variables without distinguishing them
        var_to_service = {}

        # Pattern: variable = boto3.client('service') or self.variable = boto3.client('service')
        for match in re.finditer(r'(?:self\.)?(\w+)\s*=\s*boto3\.(?:client|resource)\([\'"](\w+)[\'"]\)', code_content):
            var_name = match.group(1)
            service = match.group(2)
            var_to_service[var_name] = service

        # Step 2: Find method calls on tracked variables
        # Pattern: var.method() or self.var.method() - extract just the variable name
        for match in re.finditer(r'(?:self\.)?(\w+)\.(\w+)\(', code_content):
            var_name = match.group(1)
            method = match.group(2)

            # Check if this variable is a boto3 client/resource
            if var_name in var_to_service:
                service = var_to_service[var_name]
                full_method = f"{service}.{method}"

                if full_method in self.BOTO3_METHOD_PERMISSIONS:
                    for perm in self.BOTO3_METHOD_PERMISSIONS[full_method]:
                        required_permissions[service].add(perm)

        # Step 3: Find direct boto3 calls (e.g., boto3.client('s3').put_object())
        for match in re.finditer(r'boto3\.(?:client|resource)\([\'"](\w+)[\'"]\)\.(\w+)\(', code_content):
            service = match.group(1)
            method = match.group(2)
            full_method = f"{service}.{method}"

            if full_method in self.BOTO3_METHOD_PERMISSIONS:
                for perm in self.BOTO3_METHOD_PERMISSIONS[full_method]:
                    required_permissions[service].add(perm)

        return dict(required_permissions)

    def compare_permissions(self, code_file: str, role_name: str = None) -> Dict:
        """Compare required vs actual permissions."""
        # Read code file
        try:
            with open(code_file, 'r') as f:
                code_content = f.read()
        except FileNotFoundError:
            print(f"✗ Code file not found: {code_file}")
            raise

        # Get current identity and role
        self.get_current_identity()

        # Get role permissions
        role_permissions = self.get_role_permissions(role_name)

        # Analyze code
        print(f"\n✓ Analyzing code file: {code_file}")
        required_permissions = self.analyze_code(code_content)

        # Compare
        print("\n" + "="*60)
        print("PERMISSION ANALYSIS REPORT")
        print("="*60)

        missing_by_service = defaultdict(list)
        found_by_service = defaultdict(list)

        for service, perms in required_permissions.items():
            print(f"\n📦 Service: {service.upper()}")
            print(f"   Required Permissions: {len(perms)}")

            for perm in sorted(perms):
                # Check if permission exists
                found = False
                for resource, actions in role_permissions.items():
                    if perm in actions or f"{perm.split(':')[0]}:*" in actions or "*" in actions:
                        found = True
                        found_by_service[service].append(perm)
                        print(f"   ✓ {perm}")
                        break

                if not found:
                    missing_by_service[service].append(perm)
                    print(f"   ✗ {perm} [MISSING]")

        # Summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)

        total_required = sum(len(p) for p in required_permissions.values())
        total_missing = sum(len(p) for p in missing_by_service.values())
        total_found = sum(len(p) for p in found_by_service.values())

        print(f"Total Permissions Required: {total_required}")
        print(f"Total Permissions Found:   {total_found}")
        print(f"Total Permissions Missing: {total_missing}")

        if missing_by_service:
            print("\n⚠️  MISSING PERMISSIONS BY SERVICE:")
            for service, perms in sorted(missing_by_service.items()):
                print(f"\n   {service.upper()}:")
                for perm in sorted(perms):
                    print(f"      - {perm}")

            # Generate policy document for missing permissions
            print("\n" + "="*60)
            print("RECOMMENDED IAM POLICY (JSON)")
            print("="*60)
            self._generate_policy_document(missing_by_service)
        else:
            print("\n✓ All required permissions are available!")

        return {
            'required': required_permissions,
            'missing': dict(missing_by_service),
            'found': dict(found_by_service),
            'total': {
                'required': total_required,
                'found': total_found,
                'missing': total_missing
            }
        }

    def _generate_policy_document(self, missing_by_service: Dict[str, List[str]]):
        """Generate an IAM policy document for missing permissions."""
        statements = []

        for service, actions in sorted(missing_by_service.items()):
            # Group by resource type
            resource_mapping = {
                's3': 'arn:aws:s3:::*',
                'ec2': 'arn:aws:ec2:*:*:*',
                'dynamodb': 'arn:aws:dynamodb:*:*:table/*',
                'sns': 'arn:aws:sns:*:*:*',
                'iam': 'arn:aws:iam::*:*',
                'lambda': 'arn:aws:lambda:*:*:function/*',
                'eks': 'arn:aws:eks:*:*:cluster/*',
                'emr': 'arn:aws:elasticmapreduce:*:*:cluster/*',
                'es': 'arn:aws:es:*:*:domain/*',
            }

            statements.append({
                "Effect": "Allow",
                "Action": sorted(actions),
                "Resource": resource_mapping.get(service, '*')
            })

        policy = {
            "Version": "2012-10-17",
            "Statement": statements
        }

        print(json.dumps(policy, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description='Analyze AWS permissions required by Python code'
    )
    parser.add_argument('--code-file', required=True, help='Python file to analyze')
    parser.add_argument('--role-name', help='Specific IAM role to check (optional)')

    args = parser.parse_args()

    analyzer = AWSPermissionAnalyzer()
    analyzer.compare_permissions(args.code_file, args.role_name)


if __name__ == '__main__':
    main()
