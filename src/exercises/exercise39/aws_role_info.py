"""
AWS Role Information Tool - Display current role and all associated permissions.

Usage:
    python aws_role_info.py
    python aws_role_info.py --role-name my-role-name
"""

import boto3
import json
import argparse
from typing import Dict, List
from collections import defaultdict


class AWSRoleInfo:
    """Retrieves and displays AWS IAM role information and permissions."""

    def __init__(self):
        self.sts_client = boto3.client('sts')
        self.iam_client = boto3.client('iam')
        self.current_role = None

    def get_current_role(self) -> str:
        """Get the current IAM role name from STS."""
        try:
            identity = self.sts_client.get_caller_identity()
            arn = identity['Arn']

            # Extract role/user name from ARN
            # Format: arn:aws:iam::ACCOUNT:role/ROLE_NAME or user/USER_NAME
            role_name = arn.split('/')[-1]

            print(f"\n{'='*70}")
            print("CURRENT AWS IDENTITY")
            print(f"{'='*70}")
            print(f"ARN:        {arn}")
            print(f"Account:    {identity['Account']}")
            print(f"UserId:     {identity['UserId']}")
            print(f"Role/User:  {role_name}")

            # Check if it's a role
            if '/role/' in arn:
                self.current_role = role_name
                return role_name
            elif '/user/' in arn:
                print(f"\nℹ️  This is an IAM User, not a Role")
                return role_name

            return role_name

        except Exception as e:
            print(f"✗ Error getting current role: {e}")
            raise

    def get_role_details(self, role_name: str):
        """Get detailed information about a specific role."""
        try:
            role = self.iam_client.get_role(RoleName=role_name)

            print(f"\n{'='*70}")
            print(f"ROLE DETAILS: {role_name}")
            print(f"{'='*70}")
            print(f"Role ARN:           {role['Role']['Arn']}")
            print(f"Created:            {role['Role']['CreateDate']}")
            print(f"Max Session Duration: {role['Role']['MaxSessionDuration']} seconds")

            # Trust policy
            print(f"\nTrust Relationship (Assume Role Policy):")
            print("-" * 70)
            print(json.dumps(role['Role']['AssumeRolePolicyDocument'], indent=2))

        except Exception as e:
            print(f"✗ Error getting role details: {e}")

    def list_role_permissions(self, role_name: str):
        """List all permissions for a role."""
        print(f"\n{'='*70}")
        print(f"PERMISSIONS FOR ROLE: {role_name}")
        print(f"{'='*70}")

        try:
            # Get inline policies
            print("\n📋 INLINE POLICIES:")
            print("-" * 70)
            inline_policies = self.iam_client.list_role_policies(RoleName=role_name)

            if not inline_policies['PolicyNames']:
                print("   (No inline policies)")
            else:
                for policy_name in inline_policies['PolicyNames']:
                    print(f"\n   Policy: {policy_name}")
                    policy_doc = self.iam_client.get_role_policy(
                        RoleName=role_name,
                        PolicyName=policy_name
                    )
                    self._print_policy(policy_doc['RolePolicy']['Statement'])

            # Get managed policies
            print("\n\n📎 MANAGED POLICIES:")
            print("-" * 70)
            managed_policies = self.iam_client.list_attached_role_policies(RoleName=role_name)

            if not managed_policies['AttachedPolicies']:
                print("   (No managed policies)")
            else:
                for policy in managed_policies['AttachedPolicies']:
                    policy_arn = policy['PolicyArn']
                    policy_name = policy['PolicyName']
                    print(f"\n   Policy: {policy_name}")
                    print(f"   ARN:    {policy_arn}")

                    # Get policy details
                    policy_version = self.iam_client.get_policy(PolicyArn=policy_arn)
                    default_version_id = policy_version['Policy']['DefaultVersionId']

                    policy_doc = self.iam_client.get_policy_version(
                        PolicyArn=policy_arn,
                        VersionId=default_version_id
                    )
                    self._print_policy(policy_doc['PolicyVersion']['Document']['Statement'])

        except Exception as e:
            print(f"✗ Error listing permissions: {e}")

    def _print_policy(self, statements: List[Dict]):
        """Pretty print policy statements."""
        for i, statement in enumerate(statements):
            effect = statement.get('Effect', 'Unknown')
            actions = statement.get('Action', [])
            resources = statement.get('Resource', ['*'])

            if isinstance(actions, str):
                actions = [actions]
            if isinstance(resources, str):
                resources = [resources]

            print(f"\n      Statement {i+1}:")
            print(f"      Effect: {effect}")
            print(f"      Actions:")
            for action in actions:
                print(f"         - {action}")
            print(f"      Resources:")
            for resource in resources:
                print(f"         - {resource}")

    def summarize_permissions(self, role_name: str) -> Dict[str, int]:
        """Summarize permissions by service."""
        permissions_by_service = defaultdict(set)

        try:
            # Inline policies
            inline_policies = self.iam_client.list_role_policies(RoleName=role_name)
            for policy_name in inline_policies['PolicyNames']:
                policy_doc = self.iam_client.get_role_policy(
                    RoleName=role_name,
                    PolicyName=policy_name
                )
                self._extract_service_actions(
                    policy_doc['RolePolicy']['Statement'],
                    permissions_by_service
                )

            # Managed policies
            managed_policies = self.iam_client.list_attached_role_policies(RoleName=role_name)
            for policy in managed_policies['AttachedPolicies']:
                policy_arn = policy['PolicyArn']
                policy_version = self.iam_client.get_policy(PolicyArn=policy_arn)
                default_version_id = policy_version['Policy']['DefaultVersionId']

                policy_doc = self.iam_client.get_policy_version(
                    PolicyArn=policy_arn,
                    VersionId=default_version_id
                )
                self._extract_service_actions(
                    policy_doc['PolicyVersion']['Document']['Statement'],
                    permissions_by_service
                )

        except Exception as e:
            print(f"✗ Error summarizing permissions: {e}")

        # Print summary
        print(f"\n{'='*70}")
        print("PERMISSIONS SUMMARY BY SERVICE")
        print(f"{'='*70}")

        if permissions_by_service:
            for service in sorted(permissions_by_service.keys()):
                actions = permissions_by_service[service]
                print(f"\n{service.upper()}: {len(actions)} permissions")

                # Show first 10 permissions as examples
                for action in sorted(list(actions))[:10]:
                    print(f"   - {action}")
                if len(actions) > 10:
                    print(f"   ... and {len(actions) - 10} more")
        else:
            print("No permissions found")

        return {service: len(actions) for service, actions in permissions_by_service.items()}

    def _extract_service_actions(self, statements: List[Dict], permissions: Dict):
        """Extract service:action pairs from statements."""
        for statement in statements:
            if statement.get('Effect') == 'Allow':
                actions = statement.get('Action', [])
                if isinstance(actions, str):
                    actions = [actions]

                for action in actions:
                    if ':' in action:
                        service = action.split(':')[0]
                    else:
                        service = 'unknown'

                    permissions[service].add(action)


def main():
    parser = argparse.ArgumentParser(
        description='Display current AWS IAM role and permissions'
    )
    parser.add_argument('--role-name', help='Specific role to check (optional)')
    parser.add_argument('--details', action='store_true', help='Show detailed policy statements')

    args = parser.parse_args()

    analyzer = AWSRoleInfo()

    # Get current role
    role_name = args.role_name or analyzer.get_current_role()

    if role_name:
        # Show role details if it's a role
        try:
            analyzer.get_role_details(role_name)
        except:
            pass

        # Show permissions
        if args.details:
            analyzer.list_role_permissions(role_name)

        # Show summary
        analyzer.summarize_permissions(role_name)


if __name__ == '__main__':
    main()
