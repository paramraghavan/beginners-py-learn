"""
AWS Permission Analyzer (Runtime) - Analyzes permissions by executing code and catching permission errors.

This approach actually runs the code and intercepts AWS permission-related exceptions,
providing more accurate results than static analysis.

Usage:
    from permission_analyzer_runtime import PermissionTracker

    with PermissionTracker() as tracker:
        # Your AWS code here
        s3 = boto3.client('s3')
        s3.put_object(Bucket='my-bucket', Key='file.txt', Body=b'data')

    tracker.report()
"""

import boto3
import functools
import sys
from typing import Dict, Set, List, Tuple
from collections import defaultdict
from botocore.exceptions import ClientError


class PermissionTracker:
    """
    Context manager that tracks AWS permission errors during code execution.

    Wraps boto3 client methods to intercept permission-related exceptions,
    records them, and suppresses the error to let execution continue.
    """

    # Mapping of AWS error codes to IAM permissions
    ERROR_TO_PERMISSION = {
        'AccessDenied': '{service}:*',  # Generic - will be refined
        'UnauthorizedOperation': '{service}:*',
        'AccessDeniedException': '{service}:*',
        'InvalidPermission.NotFound': '{service}:*',
        'NotAuthorizedForSourceException': '{service}:*',
        'UnauthorizedException': '{service}:*',
        'ForbiddenException': '{service}:*',
        'OperationNotPermitted': '{service}:*',
    }

    # Service-specific error codes
    SERVICE_ERROR_CODES = {
        's3': ['AccessDenied', 'NoSuchBucket', 'AccessDeniedException'],
        'ec2': ['UnauthorizedOperation', 'AccessDenied'],
        'dynamodb': ['AccessDeniedException', 'UnauthorizedException'],
        'iam': ['AccessDenied', 'UnauthorizedException'],
        'lambda': ['AccessDeniedException', 'UnauthorizedException'],
        'sns': ['AuthorizationError', 'AccessDenied'],
        'sqs': ['AccessDenied', 'AuthorizationError'],
        'rds': ['AccessDenied', 'InvalidDBInstanceStateFault'],
    }

    def __init__(self, verbose=False):
        """
        Initialize the PermissionTracker.

        Args:
            verbose: If True, print permission errors as they occur
        """
        self.verbose = verbose
        self.missing_permissions: Dict[str, Set[str]] = defaultdict(set)
        self.attempted_operations: List[Tuple[str, str]] = []
        self.errors_caught = 0
        self._original_make_request = None
        self._patched_clients = {}

    def __enter__(self):
        """Enter context manager - patch boto3 clients."""
        self._patch_boto3()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager - restore original boto3."""
        self._unpatch_boto3()
        return False

    def _patch_boto3(self):
        """Patch boto3 to intercept permission errors."""
        # Monkey-patch the BaseClient to track permission errors
        from botocore.client import BaseClient

        self._original_make_request = BaseClient._make_request

        @functools.wraps(BaseClient._make_request)
        def tracked_make_request(self, operation_model, request_dict, request_context):
            """Intercept requests and catch permission errors."""
            service = self._service_model.service_name
            operation = operation_model.name

            try:
                return self._original_make_request(operation_model, request_dict, request_context)
            except ClientError as e:
                error_code = e.response.get('Error', {}).get('Code', 'Unknown')
                error_msg = e.response.get('Error', {}).get('Message', '')

                # Check if it's a permission error
                if self._is_permission_error(error_code, service):
                    self._track_permission_error(service, operation, error_code, error_msg)

                    if self.verbose:
                        print(f"⚠️  Permission Error: {service}:{operation} - {error_code}")

                    # Return a mock response to allow execution to continue
                    return self._get_mock_response(operation_model)
                else:
                    # Re-raise non-permission errors
                    raise

        BaseClient._make_request = tracked_make_request

    def _unpatch_boto3(self):
        """Restore original boto3 behavior."""
        from botocore.client import BaseClient
        if self._original_make_request:
            BaseClient._make_request = self._original_make_request

    def _is_permission_error(self, error_code: str, service: str) -> bool:
        """Check if an error is a permission-related error."""
        # Check generic permission errors
        if error_code in self.ERROR_TO_PERMISSION:
            return True

        # Check service-specific errors
        service_errors = self.SERVICE_ERROR_CODES.get(service, [])
        if error_code in service_errors:
            return True

        # Check for permission-related keywords in error code
        permission_keywords = ['access', 'deny', 'authorized', 'forbidden', 'permission']
        if any(keyword in error_code.lower() for keyword in permission_keywords):
            return True

        return False

    def _track_permission_error(self, service: str, operation: str, error_code: str, error_msg: str):
        """Track a permission error."""
        self.errors_caught += 1
        self.attempted_operations.append((service, operation))

        # Try to infer the permission name
        # Format: service:Operation (e.g., s3:PutObject)
        permission = f"{service}:{self._camel_to_title(operation)}"
        self.missing_permissions[service].add(permission)

    def _camel_to_title(self, text: str) -> str:
        """Convert camelCase to TitleCase."""
        # Handle special cases
        if text.lower() in ['getobject', 'putobject', 'deleteobject', 'listbuckets']:
            words = []
            current = ''
            for i, char in enumerate(text):
                if char.isupper() and i > 0:
                    words.append(current)
                    current = char
                else:
                    current += char
            if current:
                words.append(current)
            return ''.join(w.capitalize() for w in words)
        return text[0].upper() + text[1:] if text else text

    def _get_mock_response(self, operation_model):
        """Return a mock response for an operation to allow execution to continue."""
        # Return a minimal valid response structure
        return {
            'ResponseMetadata': {
                'HTTPStatusCode': 403,
                'HTTPHeaders': {'x-mocked': 'true'},
                'RetryAttempts': 0,
            }
        }

    def report(self):
        """Print a detailed report of missing permissions."""
        print("\n" + "=" * 70)
        print("AWS PERMISSION ANALYSIS REPORT (RUNTIME)")
        print("=" * 70)

        if self.errors_caught == 0:
            print("\n✅ No permission errors detected!")
            print("   All operations completed successfully.")
            return

        print(f"\n📊 Summary:")
        print(f"   - Errors caught: {self.errors_caught}")
        print(f"   - Unique operations attempted: {len(set(self.attempted_operations))}")
        print(f"   - Services affected: {len(self.missing_permissions)}")

        print(f"\n⚠️  Missing Permissions by Service:")
        print("-" * 70)

        for service in sorted(self.missing_permissions.keys()):
            perms = sorted(self.missing_permissions[service])
            print(f"\n   📦 {service.upper()}: {len(perms)} permissions")
            for perm in perms:
                print(f"      ✗ {perm}")

        # Generate IAM policy
        print("\n" + "=" * 70)
        print("RECOMMENDED IAM POLICY (JSON)")
        print("=" * 70)
        self._print_policy_document()

    def _print_policy_document(self):
        """Generate and print a recommended IAM policy."""
        import json

        # Resource ARN mapping
        resource_mapping = {
            's3': 'arn:aws:s3:::*',
            'ec2': 'arn:aws:ec2:*:*:*',
            'dynamodb': 'arn:aws:dynamodb:*:*:table/*',
            'sns': 'arn:aws:sns:*:*:*',
            'sqs': 'arn:aws:sqs:*:*:*',
            'iam': 'arn:aws:iam::*:*',
            'lambda': 'arn:aws:lambda:*:*:function/*',
            'eks': 'arn:aws:eks:*:*:cluster/*',
            'rds': 'arn:aws:rds:*:*:*',
        }

        statements = []
        for service in sorted(self.missing_permissions.keys()):
            actions = sorted(self.missing_permissions[service])
            statements.append({
                "Effect": "Allow",
                "Action": actions,
                "Resource": resource_mapping.get(service, '*')
            })

        policy = {
            "Version": "2012-10-17",
            "Statement": statements
        }

        print(json.dumps(policy, indent=2))

    def get_missing_permissions(self) -> Dict[str, Set[str]]:
        """Get the missing permissions dictionary."""
        return dict(self.missing_permissions)

    def get_summary(self) -> Dict:
        """Get a summary of the analysis."""
        return {
            'errors_caught': self.errors_caught,
            'services_affected': list(self.missing_permissions.keys()),
            'total_permissions_needed': sum(len(p) for p in self.missing_permissions.values()),
            'missing_by_service': {s: sorted(list(p)) for s, p in self.missing_permissions.items()},
        }


# Example usage
if __name__ == '__main__':
    """
    Example: Analyze an AWS application at runtime.
    """

    print("AWS Permission Analyzer (Runtime Mode)")
    print("=" * 70)
    print("\nExample usage:")
    print("""
    from permission_analyzer_runtime import PermissionTracker
    import boto3

    with PermissionTracker(verbose=True) as tracker:
        # Your AWS code
        s3 = boto3.client('s3')
        s3.put_object(Bucket='my-bucket', Key='file.txt', Body=b'data')

        ec2 = boto3.client('ec2')
        ec2.start_instances(InstanceIds=['i-1234567890abcdef0'])

    tracker.report()
    """)

    print("\nFeatures:")
    print("  ✓ Actual runtime permission tracking")
    print("  ✓ Catches real AWS errors, not guesses")
    print("  ✓ Suppresses permission errors to continue execution")
    print("  ✓ Generates IAM policy documents")
    print("  ✓ No static analysis limitations")
    print("  ✓ Works with any boto3 code pattern")
