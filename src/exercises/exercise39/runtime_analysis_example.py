"""
Example: Using the Runtime Permission Analyzer

This demonstrates how to use the runtime permission analyzer to identify
missing AWS permissions by actually executing your code and catching errors.
"""

import boto3
from permission_analyzer_runtime import PermissionTracker


def example_with_tracking():
    """Example 1: Basic usage with permission tracking."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic S3 and EC2 Operations with Tracking")
    print("="*70 + "\n")

    with PermissionTracker(verbose=True) as tracker:
        try:
            # S3 operations
            s3 = boto3.client('s3', region_name='us-east-1')

            # These will fail with permission errors (if user lacks permissions)
            # but the tracker will catch them and continue execution
            print("Attempting S3 operations...")
            s3.put_object(Bucket='my-bucket', Key='test.txt', Body=b'data')
            s3.get_object(Bucket='my-bucket', Key='test.txt')
            s3.list_objects(Bucket='my-bucket')
            s3.delete_object(Bucket='my-bucket', Key='test.txt')

            # EC2 operations
            ec2 = boto3.client('ec2', region_name='us-east-1')
            print("\nAttempting EC2 operations...")
            ec2.describe_instances()
            ec2.start_instances(InstanceIds=['i-1234567890abcdef0'])
            ec2.stop_instances(InstanceIds=['i-1234567890abcdef0'])

        except Exception as e:
            # Non-permission errors will still raise
            print(f"Unexpected error: {e}")

    # Generate report
    tracker.report()


def example_with_multiple_services():
    """Example 2: Multiple AWS services."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Multiple AWS Services")
    print("="*70 + "\n")

    with PermissionTracker(verbose=True) as tracker:
        try:
            # S3
            print("Testing S3...")
            s3 = boto3.client('s3')
            s3.put_object(Bucket='test-bucket', Key='file.txt', Body=b'content')

            # DynamoDB
            print("Testing DynamoDB...")
            dynamodb = boto3.client('dynamodb')
            dynamodb.create_table(
                TableName='test-table',
                KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
                BillingMode='PAY_PER_REQUEST'
            )
            dynamodb.put_item(
                TableName='test-table',
                Item={'id': {'S': '123'}, 'data': {'S': 'test'}}
            )

            # SNS
            print("Testing SNS...")
            sns = boto3.client('sns')
            topic = sns.create_topic(Name='test-topic')
            sns.publish(TopicArn=topic['TopicArn'], Message='Test message')

            # Lambda
            print("Testing Lambda...")
            lambda_client = boto3.client('lambda')
            lambda_client.list_functions()
            lambda_client.invoke(
                FunctionName='test-function',
                Payload=b'{"test": "data"}'
            )

        except Exception as e:
            if not isinstance(e, Exception):  # Catch unexpected errors
                raise

    tracker.report()

    # Get summary programmatically
    summary = tracker.get_summary()
    print("\n\nProgrammatic Summary:")
    print(f"Total permissions needed: {summary['total_permissions_needed']}")
    print(f"Services affected: {summary['services_affected']}")


def example_with_conditional_logic():
    """Example 3: Code with conditional logic."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Conditional Logic and Error Handling")
    print("="*70 + "\n")

    with PermissionTracker(verbose=False) as tracker:  # verbose=False for cleaner output
        try:
            s3 = boto3.client('s3')

            # Different code paths that might need different permissions
            bucket_name = 'my-app-bucket'

            # Path 1: Setup operations
            print("Running setup operations...")
            s3.create_bucket(Bucket=bucket_name)
            s3.put_bucket_versioning(
                Bucket=bucket_name,
                VersioningConfiguration={'Status': 'Enabled'}
            )

            # Path 2: Data operations
            print("Running data operations...")
            for i in range(3):
                key = f'data/file-{i}.txt'
                s3.put_object(Bucket=bucket_name, Key=key, Body=f'data-{i}'.encode())

            # Path 3: Cleanup
            print("Running cleanup...")
            s3.delete_bucket(Bucket=bucket_name)

        except Exception:
            pass

    print(f"\nTracked {tracker.errors_caught} permission errors")
    tracker.report()


def example_custom_handling():
    """Example 4: Custom handling of results."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Custom Handling and Analysis")
    print("="*70 + "\n")

    with PermissionTracker() as tracker:
        try:
            # Test various services
            services_to_test = [
                ('s3', lambda: boto3.client('s3').list_buckets()),
                ('ec2', lambda: boto3.client('ec2').describe_instances()),
                ('iam', lambda: boto3.client('iam').list_users()),
                ('dynamodb', lambda: boto3.client('dynamodb').list_tables()),
            ]

            for service_name, operation in services_to_test:
                print(f"Testing {service_name}...")
                try:
                    operation()
                except Exception:
                    pass

        except Exception:
            pass

    # Custom analysis
    summary = tracker.get_summary()

    print(f"\n📊 Custom Analysis:")
    print(f"Total errors: {summary['errors_caught']}")

    if summary['total_permissions_needed'] > 0:
        print(f"\nPermissions needed per service:")
        for service, perms in summary['missing_by_service'].items():
            print(f"  - {service}: {len(perms)} permissions")
            for perm in perms[:3]:  # Show first 3
                print(f"    • {perm}")
            if len(perms) > 3:
                print(f"    • ... and {len(perms) - 3} more")
    else:
        print("\nNo permission errors detected!")


if __name__ == '__main__':
    print("AWS Runtime Permission Analyzer - Examples")
    print("=" * 70)
    print("""
This demonstrates the runtime-based permission analyzer which:
1. Executes your actual AWS code
2. Catches permission-related exceptions
3. Suppresses them to allow execution to continue
4. Reports all permissions that would have failed
5. Generates IAM policies for those permissions

Note: These examples will only show permission errors if your AWS role
actually lacks those permissions. If you have full access, no errors
will be caught.
    """)

    # Run examples
    try:
        example_with_tracking()
    except Exception as e:
        print(f"Example 1 setup error: {e}")

    try:
        example_with_multiple_services()
    except Exception as e:
        print(f"Example 2 setup error: {e}")

    try:
        example_with_conditional_logic()
    except Exception as e:
        print(f"Example 3 setup error: {e}")

    try:
        example_custom_handling()
    except Exception as e:
        print(f"Example 4 setup error: {e}")

    print("\n" + "="*70)
    print("✅ Runtime analyzer examples complete!")
    print("="*70)
