# AWS Permission Analysis Tools

This directory contains tools to help you understand and debug AWS IAM permissions for Python applications using boto3.

## Files Overview

### 1. `sample_aws_app.py`
A sample AWS application that demonstrates common operations across multiple AWS services:
- **S3**: ListBuckets, GetObject, PutObject, DeleteObject, ListObjects
- **EC2**: DescribeInstances, StartInstances, StopInstances, CreateSecurityGroup
- **DynamoDB**: CreateTable, PutItem, GetItem, Scan
- **SNS**: CreateTopic, Publish
- **IAM**: ListUsers, ListRoles, GetUser
- **Lambda**: ListFunctions, CreateFunction, InvokeFunction, UpdateFunctionCode, DeleteFunction
- **EKS**: ListClusters, DescribeCluster, CreateCluster, DeleteCluster, ListNodegroups
- **EMR**: ListClusters, DescribeCluster, RunJobFlow, AddJobFlowSteps, TerminateJobFlows
- **Elasticsearch**: ListDomainNames, DescribeElasticsearchDomain, CreateElasticsearchDomain, DeleteElasticsearchDomain, UpdateElasticsearchDomainConfig

Use this as a reference for what operations require what permissions.

### 2. `aws_role_info.py`
Displays information about your current AWS IAM role and permissions.

**Usage:**
```bash
# Show current role and permission summary
python aws_role_info.py

# Show detailed policy statements
python aws_role_info.py --details

# Check a specific role (if you have permission)
python aws_role_info.py --role-name my-role-name --details
```

**Output includes:**
- Current identity (ARN, Account ID)
- Trust relationships
- All inline policies
- All managed policies
- Summary of permissions by service
- Count of permissions per service

### 3. `permission_analyzer.py`
The main tool - analyzes your Python code to identify required AWS permissions and compares them against your current role's permissions.

**Usage:**
```bash
# Analyze your code
python permission_analyzer.py --code-file sample_aws_app.py

# Check against a specific role
python permission_analyzer.py --code-file sample_aws_app.py --role-name my-role-name
```

**Output includes:**
- Current identity information
- Role permissions analysis
- Code analysis (identifies all boto3 calls)
- Comparison: Required vs Available permissions
- **Missing permissions** highlighted with ✗
- Recommended IAM policy document (JSON) for missing permissions

## Workflow Example

### Step 1: Understand Your Current Role
```bash
python aws_role_info.py --details
```
This shows what permissions your current role has.

### Step 2: Analyze Your Application
```bash
python permission_analyzer.py --code-file your_app.py
```
This identifies:
- What permissions your code needs
- Which permissions you already have
- What permissions are missing

### Step 3: Get the Missing Permissions
At the bottom of the analyzer output, you'll see a JSON policy document with all missing permissions. Share this with your AWS administrator.

## Understanding the Output

### Permission Format
AWS permissions follow this format: `service:Action`

Examples:
- `s3:GetObject` - Read from S3
- `s3:PutObject` - Write to S3
- `ec2:StartInstances` - Start EC2 instances
- `dynamodb:Scan` - Scan a DynamoDB table

### Permission Analysis Report
```
✓ Found permission       - You have this permission
✗ Missing permission    - You don't have this permission
```

### Generated Policy Document
The tool generates a JSON policy you can use to request additional permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::*"
    }
  ]
}
```

## Common Permission Issues

### S3 Operations
| Operation | Permission |
|-----------|-----------|
| List all buckets | `s3:ListAllMyBuckets` |
| List objects in bucket | `s3:ListBucket` |
| Read object | `s3:GetObject` |
| Write object | `s3:PutObject` |
| Delete object | `s3:DeleteObject` |

### EC2 Operations
| Operation | Permission |
|-----------|-----------|
| List instances | `ec2:DescribeInstances` |
| Start instance | `ec2:StartInstances` |
| Stop instance | `ec2:StopInstances` |
| Create security group | `ec2:CreateSecurityGroup` |

### DynamoDB Operations
| Operation | Permission |
|-----------|-----------|
| Create table | `dynamodb:CreateTable` |
| Write item | `dynamodb:PutItem` |
| Read item | `dynamodb:GetItem` |
| Update item | `dynamodb:UpdateItem` |
| Scan table | `dynamodb:Scan` |
| Query table | `dynamodb:Query` |

### Lambda Operations
| Operation | Permission |
|-----------|-----------|
| List functions | `lambda:ListFunctions` |
| Get function | `lambda:GetFunction` |
| Create function | `lambda:CreateFunction` |
| Update code | `lambda:UpdateFunctionCode` |
| Update configuration | `lambda:UpdateFunctionConfiguration` |
| Invoke function | `lambda:InvokeFunction` |
| Delete function | `lambda:DeleteFunction` |
| Add permission | `lambda:AddPermission` |

### EKS Operations
| Operation | Permission |
|-----------|-----------|
| List clusters | `eks:ListClusters` |
| Describe cluster | `eks:DescribeCluster` |
| Create cluster | `eks:CreateCluster` |
| Delete cluster | `eks:DeleteCluster` |
| Update cluster version | `eks:UpdateClusterVersion` |
| List nodegroups | `eks:ListNodegroups` |
| Create nodegroup | `eks:CreateNodegroup` |
| Delete nodegroup | `eks:DeleteNodegroup` |

### EMR Operations
| Operation | Permission |
|-----------|-----------|
| List clusters | `elasticmapreduce:ListClusters` |
| Describe cluster | `elasticmapreduce:DescribeCluster` |
| Run cluster | `elasticmapreduce:RunJobFlow` |
| Add job steps | `elasticmapreduce:AddJobFlowSteps` |
| Terminate cluster | `elasticmapreduce:TerminateJobFlows` |
| Set termination protection | `elasticmapreduce:SetTerminationProtection` |

### Elasticsearch Operations
| Operation | Permission |
|-----------|-----------|
| List domains | `es:ListDomainNames` |
| Describe domain | `es:DescribeElasticsearchDomain` |
| Create domain | `es:CreateElasticsearchDomain` |
| Delete domain | `es:DeleteElasticsearchDomain` |
| Update domain config | `es:UpdateElasticsearchDomainConfig` |
| Get domain config | `es:DescribeElasticsearchDomainConfig` |

## Customizing for Your Code

To use these tools with your own Python code:

1. Place your Python file in this directory
2. Run: `python permission_analyzer.py --code-file your_file.py`
3. The tool will extract all boto3 calls and identify required permissions

### Supported Patterns
The analyzer recognizes:
```python
# These patterns are detected:
client = boto3.client('service')
client.method_name()

resource = boto3.resource('service')
resource.method_name()

# Common assignment patterns:
self.s3_client = boto3.client('s3')
self.s3_client.put_object(...)

# Direct boto3 calls:
boto3.client('s3').put_object(...)
```

## How the Code Analyzer Works

The permission analyzer uses **3-step pattern matching** to find all boto3 operations:

### Step 1: Build Variable-to-Service Mapping

The analyzer finds all boto3 client/resource assignments and creates a mapping:

**Pattern:** `variable = boto3.client('service')`

**Example code:**
```python
s3 = boto3.client('s3')
self.lambda_client = boto3.client('lambda')
db = boto3.resource('dynamodb')
```

**Created mapping:**
```python
{
    's3': 's3',
    'lambda_client': 'lambda',
    'db': 'dynamodb'
}
```

**How it works:**
- Uses regex: `(?:self\.)?(\w+)\s*=\s*boto3\.(?:client|resource)\([\'"](\w+)[\'"]\)`
- `(?:self\.)?` - Optionally matches `self.` prefix
- `(\w+)` - Captures variable name
- `(\w+)` - Captures service name
- Treats local and instance variables the same way

  Regex Pattern:
  (?:self\.)?(\w+)\s*=\s*boto3\.(?:client|resource)\([\'"](\w+)[\'"]\)

  What it does: Finds all variable assignments to boto3 clients/resources

  Breaking down the pattern:
  - (?:self\.)? - Optionally matches self. ( (?:pattern) non-capturing group, not captured as a group) 
  - (\w+) - GROUP 1: Captures the variable name
  - \s*=\s* - Matches = with optional spaces
  - boto3\.(?:client|resource) - Matches boto3.client OR boto3.resource
  - \([\'"](\w+)[\'"]\) - GROUP 2: Captures the service name

  On our example code:

  ┌─────────────────────────────────────────────┬───────────────┬──────────┬────────────────────────────────────────────┐
  │                    Match                    │    GROUP 1    │ GROUP 2  │                   Result                   │
  ├─────────────────────────────────────────────┼───────────────┼──────────┼────────────────────────────────────────────┤
  │ s3 = boto3.client('s3')                     │ s3            │ s3       │ var_to_service['s3'] = 's3'                │
  ├─────────────────────────────────────────────┼───────────────┼──────────┼────────────────────────────────────────────┤
  │ self.lambda_client = boto3.client('lambda') │ lambda_client │ lambda   │ var_to_service['lambda_client'] = 'lambda' │
  ├─────────────────────────────────────────────┼───────────────┼──────────┼────────────────────────────────────────────┤
  │ self.db = boto3.resource('dynamodb')        │ db            │ dynamodb │ var_to_service['db'] = 'dynamodb'          │
  └─────────────────────────────────────────────┴───────────────┴──────────┴────────────────────────────────────────────┘


### Step 2: Find Method Calls on Tracked Variables

The analyzer finds all method calls and looks them up in the mapping:

**Pattern:** `variable.method()`

**Example code:**
```python
s3.put_object(Bucket='my-bucket', Key='file.txt', Body=data)
self.lambda_client.invoke(FunctionName='my-func', Payload='{}')
db.Table('users').scan()
```

**How it works:**
1. Uses regex: `(?:self\.)?(\w+)\.(\w+)\(`
2. Extracts variable name and method name
3. Looks up variable in the mapping
4. Forms `service.method` (e.g., `s3.put_object`)
5. Looks up permission in `BOTO3_METHOD_PERMISSIONS`

**Example lookup:**

| Code | Variable | Method | Lookup | Permission |
|------|----------|--------|--------|-----------|
| `s3.put_object(...)` | `s3` | `put_object` | `s3.put_object` | `s3:PutObject` |
| `self.lambda_client.invoke(...)` | `lambda_client` | `invoke` | `lambda.invoke` | `lambda:InvokeFunction` |
| `db.Table('users').scan()` | `db` | `Table` | `dynamodb.Table` | Not found* |

*Note: `Table()` is a resource method that returns another object, so direct method lookups may not capture all operations.

### Step 3: Find Direct Boto3 Calls

The analyzer also finds inline boto3 calls without variable assignment:

**Pattern:** `boto3.client('service').method()`

**Example code:**
```python
boto3.client('ec2').describe_instances()
boto3.client('s3').get_object(Bucket='bucket', Key='key')
boto3.resource('dynamodb').Table('users').scan()
```

**How it works:**
1. Uses regex: `boto3\.(?:client|resource)\([\'"](\w+)[\'"]\)\.(\w+)\(`
2. Directly extracts service and method names
3. Forms `service.method` and looks up permission

---

### Example: Complete Analysis

**Input code:**
```python
class AWSApp:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.lambda_client = boto3.client('lambda')

    def process(self):
        # Step 2: Method call on tracked variable
        self.s3.put_object(Bucket='data', Key='file.txt', Body=b'content')

        # Step 2: Method call on tracked variable
        self.lambda_client.invoke(FunctionName='handler', Payload='{}')

        # Step 3: Direct boto3 call
        boto3.client('ec2').describe_instances()
```

**Analysis process:**

**Step 1 - Mapping:**
```
s3 → s3
lambda_client → lambda
```

**Step 2 - Track variable calls:**
```
self.s3.put_object()          → s3.put_object → s3:PutObject
self.lambda_client.invoke()   → lambda.invoke → lambda:InvokeFunction
```

**Step 3 - Track direct calls:**
```
boto3.client('ec2').describe_instances() → ec2.describe_instances → ec2:DescribeInstances
```

**Final result:**
```
Required Permissions:
  - s3:PutObject
  - lambda:InvokeFunction
  - ec2:DescribeInstances
```

---

### Why This 3-Step Approach?

1. **Step 1:** Handles variable assignments (works with any variable name)
2. **Step 2:** Handles method calls on variables (most common pattern)
3. **Step 3:** Handles one-off boto3 calls without variables

This covers **all real-world Python patterns** for using boto3!

## Prerequisites

- Python 3.6+
- boto3: `pip install boto3`
- AWS credentials configured (via `~/.aws/credentials` or environment variables)

## Security Notes

- These tools only **read** from AWS (view-only operations)
- No permissions are modified or created
- All communication uses official AWS APIs
- Keep your AWS credentials secure

## Troubleshooting

### "Error: The user with name ... cannot be found"
You're trying to check a role that doesn't exist or you don't have permission to view.

### "AccessDenied" when running analyzer
Your current role doesn't have permission to call IAM APIs. Ask your administrator to grant:
- `iam:GetRole`
- `iam:ListRolePolicies`
- `iam:GetRolePolicy`
- `iam:ListAttachedRolePolicies`
- `iam:GetPolicy`
- `iam:GetPolicyVersion`
- `sts:GetCallerIdentity`

### Parser doesn't detect my boto3 calls
The analyzer uses advanced regex patterns to track variable assignments. It works with:
- ✅ Any variable naming convention (`s3`, `my_client`, `aws_ec2`, etc.)
- ✅ Both local variables (`s3 = boto3.client(...)`) and instance variables (`self.s3 = ...`)
- ✅ Both `boto3.client()` and `boto3.resource()` calls
- ✅ Direct boto3 calls without variable assignment

**If it still doesn't detect your code:**
- Make sure boto3 assignments are on a single line
- Verify methods are called with parentheses: `client.method(...)` not `client.method`
- Check that service names are in quotes: `boto3.client('s3')` not `boto3.client(service)`

For truly complex patterns (dynamic service names, variables in quotes, etc.), you can manually add required permissions to the generated policy.

## Next Steps

1. Run `python aws_role_info.py` to see your current permissions
2. Run `python permission_analyzer.py --code-file sample_aws_app.py` to see an example
3. Modify `sample_aws_app.py` to match your use case
4. Share the generated policy with your AWS administrator
