#!/usr/bin/env python3
"""
Advanced Python Security Linter
A comprehensive security linter for Python code that identifies vulnerabilities
and suggests fixes for AWS, Snowflake, HashiCorp Vault, and other services.

Usage:
    python security_linter.py --file myfile.py
    python security_linter.py --package mypackage/
    python security_linter.py --file myfile.py --fix --output report.json
"""

import ast
import os
import sys
import json
import re
import argparse
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib


@dataclass
class SecurityViolation:
    """Represents a security violation found in code"""
    file_path: str
    line_number: int
    column: int
    violation_type: str
    severity: str  # 'HIGH', 'MEDIUM', 'LOW'
    message: str
    suggestion: str
    code_snippet: str
    cwe_id: Optional[str] = None  # Common Weakness Enumeration ID


class SecurityLinter(ast.NodeVisitor):
    """Main security linter class that analyzes Python AST for security issues"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.violations: List[SecurityViolation] = []
        self.source_lines: List[str] = []
        self.current_function = None

    def analyze_file(self, content: str) -> List[SecurityViolation]:
        """Analyze a Python file for security violations"""
        self.source_lines = content.splitlines()
        try:
            tree = ast.parse(content, filename=self.file_path)
            self.visit(tree)
        except SyntaxError as e:
            self.violations.append(SecurityViolation(
                file_path=self.file_path,
                line_number=e.lineno or 0,
                column=e.offset or 0,
                violation_type="SYNTAX_ERROR",
                severity="HIGH",
                message=f"Syntax error prevents security analysis: {e.msg}",
                suggestion="Fix syntax errors before running security analysis",
                code_snippet=self._get_code_snippet(e.lineno or 0),
                cwe_id="CWE-20"
            ))
        return self.violations

    def _get_code_snippet(self, line_number: int, context: int = 2) -> str:
        """Get code snippet around the violation line"""
        start = max(0, line_number - context - 1)
        end = min(len(self.source_lines), line_number + context)
        lines = []
        for i in range(start, end):
            marker = ">>> " if i == line_number - 1 else "    "
            lines.append(f"{marker}{i + 1}: {self.source_lines[i]}")
        return "\n".join(lines)

    def _add_violation(self, node: ast.AST, violation_type: str, severity: str,
                       message: str, suggestion: str, cwe_id: str = None):
        """Add a security violation to the list"""
        self.violations.append(SecurityViolation(
            file_path=self.file_path,
            line_number=node.lineno,
            column=node.col_offset,
            violation_type=violation_type,
            severity=severity,
            message=message,
            suggestion=suggestion,
            code_snippet=self._get_code_snippet(node.lineno),
            cwe_id=cwe_id
        ))

    # Security checks for AWS services
    def visit_Call(self, node: ast.Call):
        """Check function calls for security violations"""
        self._check_aws_security(node)
        self._check_sql_injection(node)
        self._check_command_injection(node)
        self._check_deserialization(node)
        self._check_crypto_usage(node)
        self._check_vault_usage(node)
        self._check_snowflake_security(node)
        self._check_url_security(node)
        self._check_eval_usage(node)
        self.generic_visit(node)

    def _check_aws_security(self, node: ast.Call):
        """Check AWS-specific security issues"""
        if isinstance(node.func, ast.Attribute):
            # Check for hardcoded AWS credentials
            if hasattr(node.func, 'attr') and node.func.attr in ['client', 'resource']:
                for keyword in node.keywords:
                    if keyword.arg in ['aws_access_key_id', 'aws_secret_access_key']:
                        if isinstance(keyword.value, ast.Str):
                            self._add_violation(
                                node, "HARDCODED_AWS_CREDENTIALS", "HIGH",
                                "Hardcoded AWS credentials found in code",
                                "Use IAM roles, environment variables, or AWS credential files instead",
                                "CWE-798"
                            )

            # Check for overly permissive IAM policies
            if hasattr(node.func, 'attr') and 'policy' in node.func.attr.lower():
                for arg in node.args:
                    if isinstance(arg, ast.Str) and '"*"' in arg.s:
                        self._add_violation(
                            node, "OVERLY_PERMISSIVE_IAM", "HIGH",
                            "Overly permissive IAM policy detected (using '*' wildcard)",
                            "Use principle of least privilege and specify exact resources/actions",
                            "CWE-732"
                        )

    def _check_sql_injection(self, node: ast.Call):
        """Check for SQL injection vulnerabilities"""
        dangerous_sql_functions = ['execute', 'cursor', 'query', 'fetchall', 'fetchone']

        if isinstance(node.func, ast.Attribute) and node.func.attr in dangerous_sql_functions:
            for arg in node.args:
                if isinstance(arg, ast.BinOp) and isinstance(arg.op, (ast.Add, ast.Mod)):
                    self._add_violation(
                        node, "SQL_INJECTION", "HIGH",
                        "Potential SQL injection vulnerability - string concatenation in SQL query",
                        "Use parameterized queries or prepared statements",
                        "CWE-89"
                    )

    def _check_command_injection(self, node: ast.Call):
        """Check for command injection vulnerabilities"""
        dangerous_functions = ['os.system', 'subprocess.call', 'subprocess.run', 'eval', 'exec']

        func_name = self._get_function_name(node.func)
        if func_name in dangerous_functions:
            for arg in node.args:
                if isinstance(arg, ast.BinOp) or self._contains_user_input(arg):
                    self._add_violation(
                        node, "COMMAND_INJECTION", "HIGH",
                        f"Potential command injection in {func_name}",
                        "Validate and sanitize all user inputs, use subprocess with shell=False",
                        "CWE-78"
                    )

    def _check_deserialization(self, node: ast.Call):
        """Check for unsafe deserialization"""
        dangerous_deserializers = ['pickle.loads', 'pickle.load', 'cPickle.loads']

        func_name = self._get_function_name(node.func)
        if func_name in dangerous_deserializers:
            self._add_violation(
                node, "UNSAFE_DESERIALIZATION", "HIGH",
                "Unsafe deserialization detected - pickle can execute arbitrary code",
                "Use safe serialization formats like JSON, or validate pickle data source",
                "CWE-502"
            )

    def _check_crypto_usage(self, node: ast.Call):
        """Check for weak cryptographic practices"""
        weak_crypto = {
            'md5': "MD5 is cryptographically broken",
            'sha1': "SHA1 is cryptographically weak",
            'DES': "DES encryption is too weak",
            'RC4': "RC4 cipher is broken"
        }

        func_name = self._get_function_name(node.func)
        for weak_alg, message in weak_crypto.items():
            if weak_alg.lower() in func_name.lower():
                self._add_violation(
                    node, "WEAK_CRYPTOGRAPHY", "MEDIUM",
                    f"Weak cryptographic algorithm detected: {message}",
                    "Use strong algorithms like SHA-256, AES-256, or bcrypt",
                    "CWE-327"
                )

    def _check_vault_usage(self, node: ast.Call):
        """Check HashiCorp Vault security issues"""
        if isinstance(node.func, ast.Attribute):
            # Check for hardcoded Vault tokens
            for keyword in node.keywords:
                if keyword.arg in ['token', 'vault_token']:
                    if isinstance(keyword.value, ast.Str):
                        self._add_violation(
                            node, "HARDCODED_VAULT_TOKEN", "HIGH",
                            "Hardcoded Vault token found in code",
                            "Use environment variables or secure token retrieval methods",
                            "CWE-798"
                        )

            # Check for disabled TLS verification
            for keyword in node.keywords:
                if keyword.arg in ['verify', 'ssl_verify'] and isinstance(keyword.value, ast.Constant):
                    if keyword.value.value is False:
                        self._add_violation(
                            node, "DISABLED_TLS_VERIFICATION", "HIGH",
                            "TLS verification disabled for Vault connection",
                            "Enable TLS verification and use proper certificates",
                            "CWE-295"
                        )

    def _check_snowflake_security(self, node: ast.Call):
        """Check Snowflake-specific security issues"""
        func_name = self._get_function_name(node.func)

        if 'snowflake' in func_name.lower():
            # Check for hardcoded credentials
            for keyword in node.keywords:
                if keyword.arg in ['password', 'private_key', 'token']:
                    if isinstance(keyword.value, ast.Str):
                        self._add_violation(
                            node, "HARDCODED_SNOWFLAKE_CREDENTIALS", "HIGH",
                            "Hardcoded Snowflake credentials detected",
                            "Use environment variables or secure credential management",
                            "CWE-798"
                        )

            # Check for disabled SSL
            for keyword in node.keywords:
                if keyword.arg == 'insecure_mode' and isinstance(keyword.value, ast.Constant):
                    if keyword.value.value is True:
                        self._add_violation(
                            node, "INSECURE_SNOWFLAKE_CONNECTION", "HIGH",
                            "Insecure Snowflake connection detected",
                            "Use SSL/TLS for secure connections",
                            "CWE-319"
                        )

    def _check_url_security(self, node: ast.Call):
        """Check URL-related security issues like the JSON response URL example"""
        func_name = self._get_function_name(node.func)

        # Check for URLs in JSON sent to Lambda or other services
        if func_name in ['json.dumps', 'json.loads', 'requests.post', 'boto3.client']:
            for arg in node.args:
                if isinstance(arg, ast.Dict):
                    for key, value in zip(arg.keys, arg.values):
                        if (isinstance(key, ast.Str) and 'url' in key.s.lower() and
                                isinstance(value, ast.Str) and
                                any(protocol in value.s for protocol in ['http://', 'https://'])):
                            self._add_violation(
                                node, "URL_IN_JSON_PAYLOAD", "MEDIUM",
                                "URL found in JSON payload - potential SSRF vulnerability",
                                "Validate URLs against allowlist, use relative paths, or sanitize external URLs",
                                "CWE-918"
                            )

    def _check_eval_usage(self, node: ast.Call):
        """Check for dangerous eval/exec usage"""
        func_name = self._get_function_name(node.func)

        if func_name in ['eval', 'exec', 'compile']:
            self._add_violation(
                node, "DANGEROUS_EVAL", "HIGH",
                f"Dangerous use of {func_name} function detected",
                "Avoid eval/exec or implement strict input validation and sandboxing",
                "CWE-95"
            )

    def _get_function_name(self, func_node: ast.AST) -> str:
        """Get the full function name from an AST node"""
        if isinstance(func_node, ast.Name):
            return func_node.id
        elif isinstance(func_node, ast.Attribute):
            base = self._get_function_name(func_node.value) if hasattr(func_node, 'value') else ''
            return f"{base}.{func_node.attr}" if base else func_node.attr
        return ''

    def _contains_user_input(self, node: ast.AST) -> bool:
        """Check if node might contain user input"""
        user_input_indicators = ['input(', 'request.', 'args.', 'form.', 'json.', 'params.']
        node_str = ast.dump(node)
        return any(indicator in node_str for indicator in user_input_indicators)

    # Check string literals for hardcoded secrets
    def visit_Str(self, node: ast.Str):
        """Check string literals for potential secrets"""
        self._check_hardcoded_secrets(node)
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant):
        """Check constant values for potential secrets (Python 3.8+)"""
        if isinstance(node.value, str):
            self._check_hardcoded_secrets(node)
        self.generic_visit(node)

    def _check_hardcoded_secrets(self, node):
        """Check for hardcoded secrets in string literals"""
        if not hasattr(node, 'value' if hasattr(node, 'value') else 's'):
            return

        text = node.value if hasattr(node, 'value') else node.s

        # Patterns for different types of secrets
        secret_patterns = {
            'AWS_ACCESS_KEY': (r'AKIA[0-9A-Z]{16}', "AWS Access Key detected"),
            'AWS_SECRET_KEY': (r'[A-Za-z0-9/+=]{40}', "Potential AWS Secret Key detected"),
            'PRIVATE_KEY': (r'-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----', "Private key detected"),
            'API_KEY': (r'[aA][pP][iI][_-]?[kK][eE][yY][_-]?[=:]\s*[\'"][0-9a-zA-Z]{20,}[\'"]', "API key detected"),
            'PASSWORD': (
            r'[pP][aA][sS][sS][wW][oO][rR][dD][_-]?[=:]\s*[\'"][^\'\"]{8,}[\'"]', "Hardcoded password detected"),
            'TOKEN': (r'[tT][oO][kK][eE][nN][_-]?[=:]\s*[\'"][0-9a-zA-Z]{20,}[\'"]', "Token detected"),
            'DATABASE_URL': (
            r'(mysql|postgres|mongodb)://[^/\s]+:[^/\s]+@', "Database connection string with credentials"),
        }

        for secret_type, (pattern, message) in secret_patterns.items():
            if re.search(pattern, text):
                self._add_violation(
                    node, f"HARDCODED_{secret_type}", "HIGH",
                    message,
                    "Move secrets to environment variables or secure secret management",
                    "CWE-798"
                )


class SecurityReporter:
    """Generate security reports in various formats"""

    @staticmethod
    def generate_console_report(violations: List[SecurityViolation]) -> str:
        """Generate a console-friendly report"""
        if not violations:
            return "✅ No security violations found!"

        report = []
        report.append(f"\n🚨 Found {len(violations)} security violations:\n")

        # Group by severity
        by_severity = {}
        for v in violations:
            by_severity.setdefault(v.severity, []).append(v)

        for severity in ['HIGH', 'MEDIUM', 'LOW']:
            if severity in by_severity:
                report.append(f"\n{severity} SEVERITY ({len(by_severity[severity])} issues):")
                report.append("=" * 50)

                for v in by_severity[severity]:
                    report.append(f"\n📁 File: {v.file_path}")
                    report.append(f"📍 Line {v.line_number}, Column {v.column}")
                    report.append(f"🔍 Type: {v.violation_type}")
                    if v.cwe_id:
                        report.append(f"🏷️  CWE: {v.cwe_id}")
                    report.append(f"💬 {v.message}")
                    report.append(f"💡 Suggestion: {v.suggestion}")
                    report.append(f"\nCode snippet:")
                    report.append(v.code_snippet)
                    report.append("-" * 30)

        return "\n".join(report)

    @staticmethod
    def generate_json_report(violations: List[SecurityViolation]) -> str:
        """Generate a JSON report"""
        return json.dumps([asdict(v) for v in violations], indent=2)

    @staticmethod
    def generate_sarif_report(violations: List[SecurityViolation]) -> str:
        """Generate SARIF (Static Analysis Results Interchange Format) report"""
        sarif = {
            "version": "2.1.0",
            "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0.json",
            "runs": [{
                "tool": {
                    "driver": {
                        "name": "Python Security Linter",
                        "version": "1.0.0",
                        "informationUri": "https://github.com/security-linter"
                    }
                },
                "results": []
            }]
        }

        for v in violations:
            result = {
                "ruleId": v.violation_type,
                "level": v.severity.lower(),
                "message": {"text": v.message},
                "locations": [{
                    "physicalLocation": {
                        "artifactLocation": {"uri": v.file_path},
                        "region": {
                            "startLine": v.line_number,
                            "startColumn": v.column
                        }
                    }
                }]
            }
            if v.cwe_id:
                result["properties"] = {"cwe": v.cwe_id}

            sarif["runs"][0]["results"].append(result)

        return json.dumps(sarif, indent=2)


class SecurityFixer:
    """Apply automatic fixes for some security violations"""

    @staticmethod
    def suggest_fixes(violations: List[SecurityViolation]) -> Dict[str, List[str]]:
        """Generate fix suggestions organized by file"""
        fixes_by_file = {}

        for violation in violations:
            file_path = violation.file_path
            if file_path not in fixes_by_file:
                fixes_by_file[file_path] = []

            fix_suggestion = SecurityFixer._generate_fix_suggestion(violation)
            fixes_by_file[file_path].append(fix_suggestion)

        return fixes_by_file

    @staticmethod
    def _generate_fix_suggestion(violation: SecurityViolation) -> str:
        """Generate specific fix suggestion for a violation"""
        fix_templates = {
            "HARDCODED_AWS_CREDENTIALS": """
# Replace hardcoded credentials with:
import os
aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
# Or use IAM roles for EC2/Lambda
""",
            "SQL_INJECTION": """
# Replace string concatenation with parameterized query:
# Bad: cursor.execute("SELECT * FROM users WHERE id = " + user_id)
# Good: cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
""",
            "COMMAND_INJECTION": """
# Use subprocess.run with list arguments:
import subprocess
# Bad: os.system("ls " + user_input)
# Good: subprocess.run(['ls', user_input], check=True)
""",
            "WEAK_CRYPTOGRAPHY": """
# Use strong cryptographic algorithms:
import hashlib
# Bad: hashlib.md5(data)
# Good: hashlib.sha256(data)
""",
            "URL_IN_JSON_PAYLOAD": """
# Validate URLs before including in JSON:
from urllib.parse import urlparse
def validate_url(url):
    parsed = urlparse(url)
    allowed_hosts = ['trusted-domain.com', 'api.company.com']
    return parsed.netloc in allowed_hosts and parsed.scheme == 'https'
"""
        }

        template = fix_templates.get(violation.violation_type, "# Apply manual fix based on suggestion")
        return f"Line {violation.line_number}: {violation.message}\n{template}"


def analyze_file(file_path: str) -> List[SecurityViolation]:
    """Analyze a single Python file for security violations"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        linter = SecurityLinter(file_path)
        return linter.analyze_file(content)
    except Exception as e:
        return [SecurityViolation(
            file_path=file_path,
            line_number=0,
            column=0,
            violation_type="ANALYSIS_ERROR",
            severity="HIGH",
            message=f"Failed to analyze file: {str(e)}",
            suggestion="Check file encoding and syntax",
            code_snippet="",
            cwe_id="CWE-20"
        )]


def analyze_package(package_path: str) -> List[SecurityViolation]:
    """Analyze all Python files in a package/directory"""
    violations = []

    for root, dirs, files in os.walk(package_path):
        # Skip common non-source directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                violations.extend(analyze_file(file_path))

    return violations


def main():
    parser = argparse.ArgumentParser(description='Advanced Python Security Linter')
    parser.add_argument('--file', '-f', help='Analyze a single Python file')
    parser.add_argument('--package', '-p', help='Analyze all Python files in a package/directory')
    parser.add_argument('--output', '-o', help='Output file for report')
    parser.add_argument('--format', choices=['console', 'json', 'sarif'], default='console',
                        help='Report format (default: console)')
    parser.add_argument('--fix', action='store_true', help='Generate fix suggestions')
    parser.add_argument('--severity', choices=['HIGH', 'MEDIUM', 'LOW'],
                        help='Filter by minimum severity level')

    args = parser.parse_args()

    if not args.file and not args.package:
        parser.print_help()
        sys.exit(1)

    # Analyze files
    violations = []
    if args.file:
        violations = analyze_file(args.file)
    elif args.package:
        violations = analyze_package(args.package)

    # Filter by severity if specified
    if args.severity:
        severity_levels = {'LOW': 0, 'MEDIUM': 1, 'HIGH': 2}
        min_level = severity_levels[args.severity]
        violations = [v for v in violations if severity_levels[v.severity] >= min_level]

    # Generate report
    if args.format == 'console':
        report = SecurityReporter.generate_console_report(violations)
    elif args.format == 'json':
        report = SecurityReporter.generate_json_report(violations)
    elif args.format == 'sarif':
        report = SecurityReporter.generate_sarif_report(violations)

    # Output report
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report written to {args.output}")
    else:
        print(report)

    # Generate fix suggestions if requested
    if args.fix:
        fixes = SecurityFixer.suggest_fixes(violations)
        print("\n" + "=" * 60)
        print("🔧 SUGGESTED FIXES:")
        print("=" * 60)

        for file_path, file_fixes in fixes.items():
            print(f"\n📁 {file_path}:")
            for fix in file_fixes:
                print(fix)
                print("-" * 40)

    # Exit with appropriate code
    sys.exit(len(violations))


if __name__ == "__main__":
    main()


# Additional utility functions for integration with other tools

def get_open_source_linters():
    """
    List of other excellent open-source Python security linters:

    1. **Bandit** - OWASP security linter for Python
       pip install bandit
       Usage: bandit -r your_project/

    2. **Safety** - Checks dependencies for known security vulnerabilities
       pip install safety
       Usage: safety check

    3. **Semgrep** - Static analysis tool with security rules
       pip install semgrep
       Usage: semgrep --config=auto your_project/

    4. **PyLint Security Plugin** - Security-focused pylint plugin
       pip install pylint-security
       Usage: pylint --load-plugins=pylint_security your_file.py

    5. **Dlint** - Tool for encouraging best coding practices
       pip install dlint
       Usage: dlint your_file.py

    6. **PyCQA Security Linters**:
       - flake8-security
       - flake8-bandit
       pip install flake8-security flake8-bandit

    Integration example:
    ```bash
    # Run multiple linters in CI/CD
    bandit -r . -f json -o bandit-report.json
    safety check --json --output safety-report.json
    python security_linter.py --package . --format json --output custom-security-report.json
    ```
    """
    pass


# Example usage and test cases
if __name__ == "__main__":
    # Example test code with security violations (for demonstration)
    test_code = '''
import os
import json
import boto3
import requests
import hashlib

# Security violations for testing:

# 1. Hardcoded AWS credentials
client = boto3.client(
    's3',
    aws_access_key_id='AKIAIOSFODNN7EXAMPLE',
    aws_secret_access_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
)

# 2. SQL injection
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)

# 3. URL in JSON payload sent to Lambda
def send_to_lambda():
    payload = {
        "callback_url": "https://external-api.com/callback",
        "response_url": request.args.get('url')  # Potential SSRF
    }
    lambda_client.invoke(FunctionName='handler', Payload=json.dumps(payload))

# 4. Weak cryptography
password_hash = hashlib.md5(password.encode()).hexdigest()

# 5. Command injection
os.system("ls " + user_input)

# 6. Hardcoded secrets
API_KEY = "sk-1234567890abcdef1234567890abcdef"
DATABASE_URL = "postgres://user:password123@db.company.com/mydb"
'''
    print("Example violations that would be detected:")
    print("=" * 50)
    print(test_code)