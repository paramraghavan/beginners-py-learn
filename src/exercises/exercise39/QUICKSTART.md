# Quick Start Guide

## Setup (One-time)

```bash
# Install dependencies
pip install -r requirements.txt

# Verify AWS credentials are configured
aws sts get-caller-identity
```

## Step-by-Step Usage

### 1️⃣ Check Your Current AWS Role and Permissions

```bash
python aws_role_info.py
```

**Output:**
- Current AWS identity (user/role name)
- List of all permissions you have
- Count of permissions per service

### 2️⃣ Analyze Your Code

```bash
python permission_analyzer.py --code-file your_app.py
```

Replace `your_app.py` with your actual Python file.

**Output:**
```
✓ Current Identity: arn:aws:iam::123456789:role/my-role

✓ Fetching permissions for role: my-role
  - Found 2 inline policies
  - Found 1 managed policies

✓ Analyzing code file: your_app.py

============================================================
PERMISSION ANALYSIS REPORT
============================================================

📦 Service: S3
   Required Permissions: 2
   ✓ s3:GetObject
   ✓ s3:PutObject

📦 Service: EC2
   Required Permissions: 1
   ✗ ec2:StartInstances [MISSING]

============================================================
SUMMARY
============================================================
Total Permissions Required: 3
Total Permissions Found:   2
Total Permissions Missing: 1

⚠️  MISSING PERMISSIONS BY SERVICE:

   EC2:
      - ec2:StartInstances

============================================================
RECOMMENDED IAM POLICY (JSON)
============================================================
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:StartInstances"
      ],
      "Resource": "arn:aws:ec2:*:*:*"
    }
  ]
}
```

### 3️⃣ Request Missing Permissions

Copy the **RECOMMENDED IAM POLICY** JSON and share it with your AWS administrator.

They can then:
- Create an inline policy for your role
- Or attach a managed policy
- Or add permissions to an existing policy

## Test with Sample App

```bash
python permission_analyzer.py --code-file sample_aws_app.py
```

This will show you what permissions the sample app needs. It's likely you'll see some `[MISSING]` permissions.

## What Each Script Does

| Script | Purpose | Use When |
|--------|---------|----------|
| `aws_role_info.py` | View current role & permissions | You need to understand what you have access to |
| `permission_analyzer.py` | Analyze code and find missing permissions | You want to know what permissions your code needs |
| `sample_aws_app.py` | Example boto3 application | You want to see common AWS operations |

## Real-World Workflow

### Scenario: You're developing an S3 backup tool

1. **Write your code:**
```python
# backup_app.py
s3 = boto3.client('s3')
s3.get_object(Bucket='my-data', Key='file.txt')  # Read
s3.put_object(Bucket='my-backup', Key='file.txt', Body=data)  # Write
```

2. **Check what you need:**
```bash
python permission_analyzer.py --code-file backup_app.py
```

3. **See output:**
```
✓ s3:GetObject
✗ s3:PutObject [MISSING]
```

4. **Request from admin:**
Share the recommended policy with S3:PutObject permission

5. **Test again after permissions updated:**
```bash
python permission_analyzer.py --code-file backup_app.py
```

Expected: All permissions show ✓

## Common Issues & Fixes

### Issue: "NoCredentialsError"
**Solution:** Configure AWS credentials
```bash
# Option 1: Use AWS CLI
aws configure

# Option 2: Set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

### Issue: "AccessDenied" when reading role info
**Solution:** Your role needs `iam:GetRole` permission. Ask your admin to add:
```json
{
  "Effect": "Allow",
  "Action": [
    "iam:GetRole",
    "iam:ListRolePolicies",
    "iam:GetRolePolicy",
    "iam:ListAttachedRolePolicies",
    "iam:GetPolicy",
    "iam:GetPolicyVersion",
    "sts:GetCallerIdentity"
  ],
  "Resource": "*"
}
```

### Issue: Analyzer doesn't find my boto3 calls
**Solution:** The analyzer looks for specific patterns:
```python
# ✓ Works
self.s3_client = boto3.client('s3')
self.s3_client.put_object(...)

# ✓ Works
client = boto3.client('s3')
client.put_object(...)

# ⚠️  May not work
client = get_boto3_client()
client.put_object(...)
```

For complex code, manually list required permissions.

## Tips

💡 **Run analysis regularly**: Every time you add new AWS operations to your code

💡 **Use least privilege**: Only request permissions you actually need

💡 **Keep policies updated**: Remove permissions when operations are no longer used

💡 **Test in dev first**: Don't run analysis in production

💡 **Document your needs**: Keep the generated policies as documentation

## Get Help

For more details, see [README.md](README.md)

For AWS permission documentation:
- [AWS IAM Actions Reference](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html)
- [S3 Actions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-with-s3-actions.html)
- [EC2 Actions](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-supported-iam-actions.html)
- [DynamoDB Actions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/access-control-overview.html)
