Yes. The fact that `failover.py` runs successfully on the on-prem server gives you a working baseline for the migration.

However, `failover.py` alone may not be enough. You must also capture its:

* Custom Python modules
* Third-party packages
* Python version
* Configuration files
* Environment variables
* Certificates
* External commands such as `gdauth`
* File paths and working directory
* Snowflake, Ping and AD connection configuration

The simplest migration is to **copy the application source, recreate the Python environment, configure connections, and
test it manually before adding Control-M**.

# 1. Identify the exact working command

On the on-prem server, document exactly how you run it:

```bash
pwd
which python
python --version
```

Then record the command:

```bash
python failover.py
```

Or perhaps:

```bash
/path/to/python /path/to/failover.py --some-option
```

Also check the current working directory:

```bash
pwd
ls -la
```

Some Python programs depend on being executed from a specific directory.

# 2. Determine which libraries are being used

There are three types of Python libraries.

## Standard Python libraries

Examples:

```python
import os
import sys
import json
import logging
import datetime
import subprocess
import pathlib
```

You do not need to copy these. They come with Python.

You only need a compatible Python version on the edge node.

## Third-party libraries

Examples:

```python
import boto3
import requests
import snowflake.connector
import ldap3
import cryptography
```

Capture the installed packages:

```bash
python -m pip freeze > requirements.txt
```

Check for broken dependencies:

```bash
python -m pip check
```

Save the Python version:

```bash
python --version > python-version.txt
```

## Custom libraries

For example:

```python
from company_auth import get_token
from failover_utils import check_status
from snowflake_helper import connect
```

These must be copied with `failover.py`.

Look at the imports:

```bash
grep -E '^[[:space:]]*(import|from) ' failover.py
```

For each custom module, find its location:

```bash
python -c "import failover_utils; print(failover_utils.__file__)"
```

Example result:

```text
/home/user/python_lib/failover_utils.py
```

That file or package must also be migrated.

For a package:

```bash
python -c "import company_auth; print(company_auth.__path__)"
```

Do this for every internal/custom import.

# 3. Create a migration folder on the on-prem server

Suppose your files currently look like:

```text
/home/user/failover/
├── failover.py
├── failover_utils.py
├── snowflake_helper.py
├── ping_helper.py
├── ad_helper.py
└── config/
    └── failover.properties
```

Create a package for migration:

```bash
mkdir -p ~/failover_migration
```

Copy the application:

```bash
cp -R /home/user/failover/* ~/failover_migration/
```

Add the dependency information:

```bash
cd ~/failover_migration

python --version > python-version.txt
python -m pip freeze > requirements.txt
python -m pip check > pip-check.txt 2>&1
```

Capture environment variable names without capturing secret values:

```bash
env | cut -d= -f1 | sort > environment-variable-names.txt
```

Create the archive:

```bash
cd ~
tar -czf failover_migration.tar.gz failover_migration
```

Do not include:

* Existing virtual environment
* Python cache files
* Old logs
* Temporary files
* Plaintext passwords
* Cached Ping tokens
* AWS access keys
* Kerberos ticket caches

If the application is already in Git, using the Git repository is cleaner than creating a tar file.

# 4. Copy it to the AWS edge node

From the on-prem server:

```bash
scp ~/failover_migration.tar.gz your-user@aws-edge-node:/tmp/
```

Or from your workstation, transfer it through your organization’s approved mechanism.

On the AWS edge node:

```bash
sudo mkdir -p /opt/failover
sudo tar -xzf /tmp/failover_migration.tar.gz \
    -C /opt/failover \
    --strip-components=1
```

Check the files:

```bash
find /opt/failover -maxdepth 3 -type f
```

# 5. Install a matching Python version

For the first migration, use the same Python major and minor version as on-prem.

For example, when on-prem uses:

```text
Python 3.11.9
```

Use Python 3.11 on the edge node.

Check:

```bash
python3.11 --version
```

Do not combine the server migration with a Python upgrade. First get the service running with the same version. Upgrade
it later as a separate change.

# 6. Create a new virtual environment

Do not copy the on-prem virtual environment.

On the edge node:

```bash
python3.11 -m venv /opt/failover/venv
```

Upgrade packaging tools:

```bash
/opt/failover/venv/bin/python -m pip install --upgrade pip setuptools wheel
```

Install dependencies:

```bash
/opt/failover/venv/bin/python -m pip install \
    -r /opt/failover/requirements.txt
```

Check dependencies:

```bash
/opt/failover/venv/bin/python -m pip check
```

# 7. Test custom module imports

Before running the actual job, test that the modules load:

```bash
cd /opt/failover

/opt/failover/venv/bin/python - <<'PY'
import failover_utils
import snowflake_helper
import ping_helper
import ad_helper

print("All custom modules imported successfully")
PY
```

Adjust the module names based on your actual application.

If custom libraries are stored in a separate directory, the cleaner structure is:

```text
/opt/failover/
├── failover.py
├── requirements.txt
├── custom_modules/
│   ├── company_auth/
│   ├── snowflake_helper/
│   └── failover_utils/
└── venv/
```

Temporarily, you can set:

```bash
export PYTHONPATH=/opt/failover/custom_modules
```

But a cleaner long-term approach is packaging the custom modules as installable Python packages.

# 8. Separate migration from authentication changes

To reduce risk, separate the work into two stages.

## Stage 1: Application migration

First prove that:

* Python works
* Third-party packages install
* Custom modules import
* Configuration files can be read
* Paths are correct
* Logging works

## Stage 2: Connection migration

Then handle:

* AWS authentication
* Snowflake authentication
* Ping tokens
* Active Directory connections

This makes troubleshooting easier. Otherwise, when the job fails, you may not know whether the cause is code,
dependencies, networking, or authentication.

# 9. Replace `gdauth` for AWS access

Because the edge node already has an IAM service role, Boto3 should generally use it automatically.

Existing code may look like:

```python
credentials = run_gdauth()

session = boto3.Session(
    aws_access_key_id=credentials.access_key,
    aws_secret_access_key=credentials.secret_key,
    aws_session_token=credentials.session_token,
)
```

On the edge node, this can usually become:

```python
import boto3

session = boto3.Session()
s3_client = session.client("s3")
```

Test the role:

```bash
/opt/failover/venv/bin/python - <<'PY'
import boto3

sts = boto3.client("sts")
print(sts.get_caller_identity())
PY
```

Also test using the eventual Control-M execution user, because IAM access can work under your root shell while other
files or configuration remain inaccessible to the Control-M account.

Do not remove all `gdauth` code until you confirm whether it is used only for AWS or also for Ping, Snowflake, or
internal API authentication.

# 10. Identify external configuration used by `failover.py`

Search the code:

```bash
cd /opt/failover

grep -RniE \
'gdauth|snowflake|ping|oauth|ldap|kerberos|keytab|boto3|password|token|certificate|pem|proxy|/home/|/data/' \
.
```

Look for things such as:

```python
open("/home/olduser/config.ini")
```

```python
os.environ["PING_TOKEN"]
```

```python
subprocess.run(["gdauth", ...])
```

```python
snowflake.connector.connect(...)
```

```python
ldap3.Server(...)
```

Replace old-server-specific paths such as:

```text
/home/brownfield-user/...
/apps/oldserver/...
/data/brownfield/...
```

with edge-node paths such as:

```text
/opt/failover/...
/etc/failover/...
/var/log/failover/...
```

# 11. Handle secrets separately

Do not copy secrets directly inside the migration archive.

Recommended:

* AWS credentials: IAM role
* Ping client secret: AWS Secrets Manager
* AD service-account password: AWS Secrets Manager
* Snowflake private key or password: AWS Secrets Manager
* Non-secret hostnames and database names: configuration file

Example non-secret configuration:

```bash
# /etc/failover/failover.env

AWS_REGION=us-east-1

SNOWFLAKE_ACCOUNT=my-account
SNOWFLAKE_DATABASE=OPERATIONS
SNOWFLAKE_SCHEMA=FAILOVER
SNOWFLAKE_WAREHOUSE=FAILOVER_WH

PING_TOKEN_URL=https://ping.example.com/token
AD_URL=ldaps://ad.example.com
```

# 12. Test without running the full failover action

Ideally add a connection-test option:

```bash
/opt/failover/venv/bin/python \
    /opt/failover/failover.py \
    --test-connections
```

This should test:

* AWS role
* Snowflake login
* Ping token retrieval
* AD connection
* Required files
* Required directories

If modifying the code is not immediately possible, at least test imports:

```bash
/opt/failover/venv/bin/python -m py_compile \
    /opt/failover/failover.py
```

Then test individual connections through small scripts before running the full job.

# 13. Run the exact command manually

Run it first from its application directory:

```bash
cd /opt/failover

/opt/failover/venv/bin/python failover.py
```

Do not initially run:

```bash
python failover.py
```

Using the full virtual-environment path guarantees that the correct Python installation is used.

Capture the output:

```bash
cd /opt/failover

/opt/failover/venv/bin/python failover.py \
    > /tmp/failover-test.log 2>&1

echo $?
```

Review:

```bash
cat /tmp/failover-test.log
```

# 14. Create a simple Control-M wrapper

Create:

```bash
/opt/failover/run_failover.sh
```

Contents:

```bash
#!/usr/bin/env bash

set -euo pipefail

APP_HOME="/opt/failover"
PYTHON="$APP_HOME/venv/bin/python"
SCRIPT="$APP_HOME/failover.py"

export PYTHONUNBUFFERED=1

cd "$APP_HOME"

echo "Failover job started: $(date -Is)"

"$PYTHON" "$SCRIPT"
exit_code=$?

echo "Failover job completed: $(date -Is)"
echo "Exit code: $exit_code"

exit "$exit_code"
```

Set permissions:

```bash
sudo chmod 750 /opt/failover/run_failover.sh
```

Control-M should execute:

```bash
/opt/failover/run_failover.sh
```

# Minimum migration package

At minimum, migrate:

```text
failover.py
custom Python modules
requirements.txt
non-secret configuration files
certificates or CA files when required
run_failover.sh
documentation of environment variables
```

Do not migrate:

```text
old virtual environment
standard Python library files
cached credentials
AWS keys
cached Ping access tokens
Kerberos ticket caches
old server logs
__pycache__ directories
```

# Simplest practical migration sequence

```text
1. Run failover.py successfully on-prem and record the exact command.
2. Capture Python version and pip freeze.
3. Find and collect every custom imported module.
4. Copy the application source to the edge node.
5. Install the same Python version.
6. Create a new virtual environment.
7. Install requirements.txt.
8. Test imports.
9. Configure Snowflake, Ping and AD connections.
10. Use the edge-node IAM role instead of gdauth for AWS.
11. Run failover.py manually.
12. Run it using the Control-M service account.
13. Schedule it through Control-M.
14. Keep the on-prem job disabled but available for rollback until validation completes.
```

So, **yes, use the working on-prem `failover.py` execution as the input and baseline for migration**, but collect its
complete runtime environment and dependencies rather than copying only the Python file.
