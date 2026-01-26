#!/usr/bin/env python3
"""
Local Security Scanner - Mimics Fortify SCA Checks
This tool scans Python files for common security vulnerabilities
that Fortify typically flags, allowing you to fix issues locally
before running the actual Fortify scan in Jenkins.
"""

import ast
import re
import sys
import os
from pathlib import Path
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict
import json

@dataclass
class SecurityIssue:
    """Represents a security vulnerability"""
    category: str
    severity: str  # Critical, High, Medium, Low
    file_path: str
    line_number: int
    code_snippet: str
    description: str
    recommendation: str
    cwe_id: str = ""

class FortifyMockScanner(ast.NodeVisitor):
    """AST-based security scanner for Python code"""
    
    def __init__(self, file_path: str, source_code: str):
        self.file_path = file_path
        self.source_code = source_code
        self.source_lines = source_code.split('\n')
        self.issues: List[SecurityIssue] = []
        self.imports: Set[str] = set()
        self.function_calls: List[Tuple[str, int]] = []
        
    def get_line_content(self, line_num: int) -> str:
        """Get source code line"""
        if 0 < line_num <= len(self.source_lines):
            return self.source_lines[line_num - 1].strip()
        return ""
    
    def add_issue(self, category: str, severity: str, line: int, 
                  description: str, recommendation: str, cwe_id: str = ""):
        """Add a security issue"""
        self.issues.append(SecurityIssue(
            category=category,
            severity=severity,
            file_path=self.file_path,
            line_number=line,
            code_snippet=self.get_line_content(line),
            description=description,
            recommendation=recommendation,
            cwe_id=cwe_id
        ))
    
    # SQL INJECTION DETECTION
    def visit_Call(self, node):
        """Check function calls for security issues"""
        func_name = self._get_func_name(node)
        
        # SQL Injection checks
        self._check_sql_injection(node, func_name)
        
        # Command Injection checks
        self._check_command_injection(node, func_name)
        
        # Path Traversal checks
        self._check_path_traversal(node, func_name)
        
        # XML/XXE checks
        self._check_xml_issues(node, func_name)
        
        # Deserialization checks
        self._check_unsafe_deserialization(node, func_name)
        
        # Cryptography checks
        self._check_weak_crypto(node, func_name)
        
        # Random number checks
        self._check_weak_random(node, func_name)
        
        self.generic_visit(node)
    
    def _get_func_name(self, node) -> str:
        """Extract function name from call node"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return ""
    
    def _check_sql_injection(self, node, func_name):
        """Check for SQL injection vulnerabilities"""
        sql_methods = ['execute', 'executemany', 'raw', 'RawSQL']
        
        if func_name in sql_methods and node.args:
            arg = node.args[0]
            
            # Check for string concatenation or f-strings in SQL
            if isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Add):
                self.add_issue(
                    category="SQL Injection",
                    severity="Critical",
                    line=node.lineno,
                    description="SQL query constructed using string concatenation with potentially unsafe input",
                    recommendation="Use parameterized queries with placeholders (?, %s) instead of string concatenation",
                    cwe_id="CWE-89"
                )
            elif isinstance(arg, ast.JoinedStr):  # f-string
                self.add_issue(
                    category="SQL Injection",
                    severity="Critical",
                    line=node.lineno,
                    description="SQL query uses f-string interpolation which is vulnerable to injection",
                    recommendation="Use parameterized queries: cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))",
                    cwe_id="CWE-89"
                )
            elif isinstance(arg, ast.Call) and self._get_func_name(arg) == 'format':
                self.add_issue(
                    category="SQL Injection",
                    severity="Critical",
                    line=node.lineno,
                    description="SQL query uses .format() method which is vulnerable to injection",
                    recommendation="Use parameterized queries instead of .format()",
                    cwe_id="CWE-89"
                )
    
    def _check_command_injection(self, node, func_name):
        """Check for command injection vulnerabilities"""
        dangerous_funcs = ['system', 'popen', 'exec', 'eval', 'compile', 
                          'execfile', '__import__']
        
        if func_name in dangerous_funcs:
            self.add_issue(
                category="Command Injection / Code Injection",
                severity="Critical",
                line=node.lineno,
                description=f"Use of dangerous function '{func_name}()' that can execute arbitrary code",
                recommendation=f"Avoid using {func_name}(). Use safer alternatives like subprocess.run() with shell=False",
                cwe_id="CWE-78"
            )
        
        # Check subprocess calls
        if func_name in ['call', 'run', 'Popen', 'check_output']:
            # Check for shell=True
            for keyword in node.keywords:
                if keyword.arg == 'shell' and isinstance(keyword.value, ast.Constant):
                    if keyword.value.value is True:
                        self.add_issue(
                            category="Command Injection",
                            severity="High",
                            line=node.lineno,
                            description="subprocess call with shell=True is dangerous if input is not validated",
                            recommendation="Use shell=False and pass command as a list: subprocess.run(['ls', '-l'])",
                            cwe_id="CWE-78"
                        )
    
    def _check_path_traversal(self, node, func_name):
        """Check for path traversal and path manipulation vulnerabilities"""
        # File operation functions
        file_funcs = ['open', 'read', 'write', 'remove', 'unlink', 'rmdir', 
                     'chmod', 'chown', 'rename', 'replace', 'makedirs', 'mkdir']
        
        # Path construction functions
        path_funcs = ['join', 'Path']
        
        if func_name in file_funcs and node.args:
            arg = node.args[0]
            
            # Get the source code context around this line
            context_start = max(0, node.lineno - 10)
            context_end = min(len(self.source_lines), node.lineno + 3)
            context = '\n'.join(self.source_lines[context_start:context_end])
            
            # Look for validation patterns in nearby code
            validation_patterns = [
                r'if\s+.*not in.*:',  # allowlist check
                r'if\s+.*in\s+\[',     # list check
                r'if\s+.*in\s+\{',     # dict check
                r'startswith\(',       # prefix check
                r'\.resolve\(\)',      # path resolution
                r'abspath\(',          # absolute path
                r'normpath\(',         # normalize path
                r'realpath\(',         # real path
                r'raise\s+ValueError', # validation error
                r'ALLOWED_',           # allowlist constant
                r'WHITELIST',          # whitelist constant
                r'basename\(',         # sanitization
                r'if\s+["\']..["\']',  # checking for ..
            ]
            
            has_validation = any(re.search(pattern, context, re.IGNORECASE) 
                               for pattern in validation_patterns)
            
            # Check if path is constructed dynamically
            if isinstance(arg, (ast.BinOp, ast.JoinedStr, ast.Call)):
                # Check for os.path.join or Path operations
                if isinstance(arg, ast.Call):
                    call_name = self._get_func_name(arg)
                    if call_name in path_funcs:
                        # Check if any argument comes from potentially untrusted source
                        has_untrusted_input = False
                        for call_arg in arg.args:
                            if isinstance(call_arg, (ast.Name, ast.Call, ast.Attribute, ast.Subscript)):
                                # Check if it's from untrusted sources
                                if isinstance(call_arg, ast.Call):
                                    inner_func = self._get_func_name(call_arg)
                                    if inner_func in ['getenv', 'input', 'raw_input', 'argv']:
                                        has_untrusted_input = True
                                        break
                                elif isinstance(call_arg, ast.Subscript):
                                    # Check for sys.argv
                                    if isinstance(call_arg.value, ast.Attribute):
                                        has_untrusted_input = True
                                        break
                                else:
                                    # Variable that could be user input
                                    has_untrusted_input = True
                        
                        if has_untrusted_input and not has_validation:
                            self.add_issue(
                                category="Path Manipulation / Path Traversal",
                                severity="High",
                                line=node.lineno,
                                description="File path constructed from external/variable input without validation",
                                recommendation="Validate paths: use allowlist, resolve() with prefix check, sanitize with basename(), prevent '..' and absolute paths",
                                cwe_id="CWE-22"
                            )
                
                # Check for string concatenation or f-strings (always flag these)
                elif isinstance(arg, (ast.BinOp, ast.JoinedStr)):
                    if not has_validation:
                        self.add_issue(
                            category="Path Manipulation / Path Traversal",
                            severity="High",
                            line=node.lineno,
                            description="File path constructed using string concatenation without validation",
                            recommendation="Use os.path.join() or pathlib.Path() and validate against allowlist",
                            cwe_id="CWE-22"
                        )
            
            # Check if path comes from variable without validation
            elif isinstance(arg, (ast.Name, ast.Attribute, ast.Subscript)):
                # Only flag if it looks like it could be from external source
                # and there's no validation
                if not has_validation:
                    # Check if variable name suggests external input
                    var_name = ""
                    if isinstance(arg, ast.Name):
                        var_name = arg.id.lower()
                    
                    suspicious_names = ['user', 'input', 'request', 'argv', 'param', 
                                       'arg', 'file', 'path', 'dir', 'config']
                    
                    if any(name in var_name for name in suspicious_names):
                        self.add_issue(
                            category="Path Manipulation / Path Traversal",
                            severity="Medium",
                            line=node.lineno,
                            description="File operation using path from variable without visible validation",
                            recommendation="Add path validation: ensure path is within allowed directory, use resolve() and check prefix",
                            cwe_id="CWE-22"
                        )
        
        # Check os.path.join and Path() calls directly for untrusted sources
        if func_name in path_funcs:
            has_untrusted_input = False
            
            for arg in node.args:
                # Check for clearly untrusted sources
                if isinstance(arg, ast.Call):
                    inner_func = self._get_func_name(arg)
                    if inner_func in ['input', 'raw_input', 'getenv']:
                        has_untrusted_input = True
                        break
                elif isinstance(arg, ast.Subscript):
                    # Check for sys.argv or request params
                    if isinstance(arg.value, ast.Attribute):
                        attr = arg.value
                        if isinstance(attr.value, ast.Name) and attr.value.id == 'sys' and attr.attr == 'argv':
                            has_untrusted_input = True
                            break
            
            # Check context for validation
            context_start = max(0, node.lineno - 10)
            context_end = min(len(self.source_lines), node.lineno + 3)
            context = '\n'.join(self.source_lines[context_start:context_end])
            
            validation_patterns = [
                r'if\s+.*not in.*:',
                r'if\s+.*in\s+\[',
                r'if\s+.*in\s+\{',
                r'ALLOWED_',
                r'raise\s+ValueError',
            ]
            
            has_validation = any(re.search(pattern, context, re.IGNORECASE) 
                               for pattern in validation_patterns)
            
            # Flag paths constructed from untrusted input without validation
            if has_untrusted_input and not has_validation:
                self.add_issue(
                    category="Path Manipulation / Path Traversal",
                    severity="High",
                    line=node.lineno,
                    description="Path constructed from external input without validation",
                    recommendation="Validate input: use allowlist, check for '..' and absolute paths, use resolve() and verify prefix",
                    cwe_id="CWE-22"
                )
    
    def _check_xml_issues(self, node, func_name):
        """Check for XML External Entity (XXE) vulnerabilities"""
        if func_name in ['parse', 'fromstring', 'XMLParser']:
            # Check if using unsafe XML parser
            if any(imp in self.imports for imp in ['xml.etree.ElementTree', 'xml.dom.minidom', 'xml.sax']):
                self.add_issue(
                    category="XML External Entity (XXE)",
                    severity="High",
                    line=node.lineno,
                    description="XML parsing without disabling external entity processing",
                    recommendation="Use defusedxml library or disable external entities: parser.setFeature(feature_external_ges, False)",
                    cwe_id="CWE-611"
                )
    
    def _check_unsafe_deserialization(self, node, func_name):
        """Check for unsafe deserialization"""
        if func_name in ['loads', 'load', 'Unpickler']:
            if 'pickle' in self.imports or 'cPickle' in self.imports:
                self.add_issue(
                    category="Unsafe Deserialization",
                    severity="Critical",
                    line=node.lineno,
                    description="Deserializing untrusted data with pickle can lead to arbitrary code execution",
                    recommendation="Use safer serialization like JSON, or validate data source before unpickling",
                    cwe_id="CWE-502"
                )
    
    def _check_weak_crypto(self, node, func_name):
        """Check for weak cryptographic algorithms"""
        weak_algos = ['MD5', 'SHA1', 'md5', 'sha1', 'DES', 'RC4']
        
        if func_name in ['new', 'hash'] and node.args:
            if isinstance(node.args[0], ast.Constant):
                algo = node.args[0].value
                if any(weak in str(algo).upper() for weak in weak_algos):
                    self.add_issue(
                        category="Weak Cryptography",
                        severity="High",
                        line=node.lineno,
                        description=f"Use of weak cryptographic algorithm: {algo}",
                        recommendation="Use strong algorithms: SHA-256, SHA-384, SHA-512, or bcrypt for passwords",
                        cwe_id="CWE-327"
                    )
    
    def _check_weak_random(self, node, func_name):
        """Check for weak random number generation"""
        if func_name in ['random', 'randint', 'choice', 'shuffle']:
            if 'random' in self.imports:
                self.add_issue(
                    category="Weak Random Number Generator",
                    severity="Medium",
                    line=node.lineno,
                    description="Using 'random' module for security-sensitive operations",
                    recommendation="Use secrets module for cryptographic purposes: secrets.token_bytes(), secrets.choice()",
                    cwe_id="CWE-330"
                )
    
    # HARDCODED CREDENTIALS DETECTION
    def visit_Assign(self, node):
        """Check assignments for hardcoded secrets"""
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id.lower()
                
                # Check for password/secret variable names
                sensitive_patterns = ['password', 'passwd', 'pwd', 'secret', 
                                     'api_key', 'apikey', 'token', 'private_key',
                                     'access_key', 'auth']
                
                if any(pattern in var_name for pattern in sensitive_patterns):
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        # Avoid flagging obviously placeholder values
                        value = node.value.value.lower()
                        if value and value not in ['', 'none', 'null', 'todo', 'changeme', 'your_password_here']:
                            self.add_issue(
                                category="Hardcoded Password/Secret",
                                severity="Critical",
                                line=node.lineno,
                                description=f"Hardcoded credential in variable '{target.id}'",
                                recommendation="Use environment variables or secure configuration management: os.getenv('API_KEY')",
                                cwe_id="CWE-798"
                            )
        
        self.generic_visit(node)
    
    # IMPORT TRACKING
    def visit_Import(self, node):
        """Track imports"""
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """Track from imports"""
        if node.module:
            self.imports.add(node.module)
        self.generic_visit(node)

class RegexScanner:
    """Regex-based scanner for patterns AST can't catch"""
    
    def __init__(self, file_path: str, source_code: str):
        self.file_path = file_path
        self.source_code = source_code
        self.lines = source_code.split('\n')
        self.issues: List[SecurityIssue] = []
    
    def scan(self):
        """Run regex-based scans"""
        self._check_hardcoded_secrets()
        self._check_debug_code()
        self._check_insecure_protocols()
        self._check_temp_files()
        self._check_path_manipulation_patterns()
        return self.issues
    
    def _check_hardcoded_secrets(self):
        """Check for hardcoded secrets using regex"""
        patterns = [
            (r'["\']([A-Za-z0-9+/]{40,})["\']', 'Possible hardcoded API key or token'),
            (r'aws_access_key_id\s*=\s*["\']([A-Z0-9]{20})["\']', 'AWS Access Key'),
            (r'aws_secret_access_key\s*=\s*["\']([A-Za-z0-9/+=]{40})["\']', 'AWS Secret Key'),
            (r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----', 'Private key in code'),
        ]
        
        for i, line in enumerate(self.lines, 1):
            for pattern, description in patterns:
                if re.search(pattern, line):
                    self.issues.append(SecurityIssue(
                        category="Hardcoded Secret",
                        severity="Critical",
                        file_path=self.file_path,
                        line_number=i,
                        code_snippet=line.strip(),
                        description=description,
                        recommendation="Remove hardcoded secrets. Use environment variables or secret management",
                        cwe_id="CWE-798"
                    ))
    
    def _check_debug_code(self):
        """Check for debug code left in production"""
        debug_patterns = [
            (r'print\s*\(.*password.*\)', 'Printing password to console'),
            (r'print\s*\(.*secret.*\)', 'Printing secret to console'),
            (r'console\.log\(.*password.*\)', 'Logging password'),
            (r'import\s+pdb', 'Debug import (pdb)'),
            (r'breakpoint\(\)', 'Debug breakpoint'),
        ]
        
        for i, line in enumerate(self.lines, 1):
            for pattern, description in debug_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self.issues.append(SecurityIssue(
                        category="Information Exposure",
                        severity="Medium",
                        file_path=self.file_path,
                        line_number=i,
                        code_snippet=line.strip(),
                        description=description,
                        recommendation="Remove debug code before production deployment",
                        cwe_id="CWE-489"
                    ))
    
    def _check_insecure_protocols(self):
        """Check for insecure protocols"""
        for i, line in enumerate(self.lines, 1):
            if re.search(r'http://(?!localhost|127\.0\.0\.1)', line, re.IGNORECASE):
                self.issues.append(SecurityIssue(
                    category="Insecure Protocol",
                    severity="Medium",
                    file_path=self.file_path,
                    line_number=i,
                    code_snippet=line.strip(),
                    description="Using insecure HTTP protocol instead of HTTPS",
                    recommendation="Use HTTPS for all external communications",
                    cwe_id="CWE-319"
                ))
    
    def _check_temp_files(self):
        """Check for insecure temp file usage"""
        if re.search(r'mktemp|tempnam', self.source_code):
            for i, line in enumerate(self.lines, 1):
                if 'mktemp' in line or 'tempnam' in line:
                    self.issues.append(SecurityIssue(
                        category="Insecure Temp File",
                        severity="Medium",
                        file_path=self.file_path,
                        line_number=i,
                        code_snippet=line.strip(),
                        description="Insecure temporary file creation",
                        recommendation="Use tempfile.mkstemp() or tempfile.TemporaryFile()",
                        cwe_id="CWE-377"
                    ))
    
    def _check_path_manipulation_patterns(self):
        """Check for path manipulation using regex patterns"""
        # Pattern for paths without validation
        path_patterns = [
            (r'open\s*\(\s*["\']?[\w/]+["\']?\s*\+\s*\w+', 'Path constructed with string concatenation'),
            (r'open\s*\(\s*f["\'].*\{.*\}.*["\']', 'Path constructed with f-string without validation'),
            (r'Path\s*\(\s*\w+\s*\)', 'Creating Path from variable without validation'),
            (r'os\.path\.join\s*\(.*os\.getenv.*\)', 'Path construction using environment variable'),
            (r'os\.path\.join\s*\(.*input\(.*\)', 'Path construction from user input'),
            (r'open\s*\(\s*sys\.argv\[', 'Opening file using command-line argument without validation'),
        ]
        
        for i, line in enumerate(self.lines, 1):
            for pattern, description in path_patterns:
                if re.search(pattern, line):
                    # Skip if there's validation nearby (basic heuristic)
                    context_start = max(0, i - 3)
                    context_end = min(len(self.lines), i + 2)
                    context = '\n'.join(self.lines[context_start:context_end])
                    
                    # Look for validation keywords
                    validation_keywords = ['allowlist', 'whitelist', 'startswith', 'resolve()', 
                                         'abspath', 'normpath', 'realpath', 'if.*in.*[', 
                                         'raise', 'ValueError', 'check', 'validate']
                    
                    has_validation = any(kw in context.lower() for kw in validation_keywords)
                    
                    if not has_validation:
                        self.issues.append(SecurityIssue(
                            category="Path Manipulation / Path Traversal",
                            severity="Medium",
                            file_path=self.file_path,
                            line_number=i,
                            code_snippet=line.strip(),
                            description=description,
                            recommendation="Add path validation: use allowlist, check for '..' and absolute paths, use resolve()",
                            cwe_id="CWE-22"
                        ))

class SecurityReportGenerator:
    """Generate security scan reports"""
    
    def __init__(self, all_issues: List[SecurityIssue]):
        self.all_issues = all_issues
        self.stats = self._calculate_stats()
    
    def _calculate_stats(self) -> Dict:
        """Calculate statistics"""
        stats = {
            'total': len(self.all_issues),
            'by_severity': defaultdict(int),
            'by_category': defaultdict(int),
            'by_file': defaultdict(int)
        }
        
        for issue in self.all_issues:
            stats['by_severity'][issue.severity] += 1
            stats['by_category'][issue.category] += 1
            stats['by_file'][issue.file_path] += 1
        
        return stats
    
    def print_console_report(self):
        """Print report to console"""
        print("\n" + "="*80)
        print("SECURITY SCAN RESULTS (Fortify-Style)")
        print("="*80 + "\n")
        
        # Summary
        print("SUMMARY:")
        print(f"  Total Issues Found: {self.stats['total']}")
        print(f"  Critical: {self.stats['by_severity']['Critical']}")
        print(f"  High: {self.stats['by_severity']['High']}")
        print(f"  Medium: {self.stats['by_severity']['Medium']}")
        print(f"  Low: {self.stats['by_severity']['Low']}")
        print()
        
        # Issues by category
        if self.stats['by_category']:
            print("ISSUES BY CATEGORY:")
            for category, count in sorted(self.stats['by_category'].items(), 
                                         key=lambda x: x[1], reverse=True):
                print(f"  {category}: {count}")
            print()
        
        # Detailed issues
        if self.all_issues:
            print("="*80)
            print("DETAILED FINDINGS:")
            print("="*80 + "\n")
            
            # Sort by severity
            severity_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
            sorted_issues = sorted(self.all_issues, 
                                 key=lambda x: (severity_order.get(x.severity, 4), 
                                              x.file_path, x.line_number))
            
            for i, issue in enumerate(sorted_issues, 1):
                print(f"[{i}] {issue.severity.upper()}: {issue.category}")
                print(f"    File: {issue.file_path}")
                print(f"    Line: {issue.line_number}")
                print(f"    Code: {issue.code_snippet}")
                print(f"    Issue: {issue.description}")
                print(f"    Fix: {issue.recommendation}")
                if issue.cwe_id:
                    print(f"    CWE: {issue.cwe_id}")
                print()
        else:
            print("✓ No security issues found!")
        
        print("="*80)
        
        # Return exit code based on severity
        if self.stats['by_severity']['Critical'] > 0:
            return 2
        elif self.stats['by_severity']['High'] > 0:
            return 1
        return 0
    
    def generate_json_report(self, output_file: str):
        """Generate JSON report"""
        report = {
            'summary': dict(self.stats),
            'issues': [
                {
                    'category': issue.category,
                    'severity': issue.severity,
                    'file': issue.file_path,
                    'line': issue.line_number,
                    'code': issue.code_snippet,
                    'description': issue.description,
                    'recommendation': issue.recommendation,
                    'cwe': issue.cwe_id
                }
                for issue in self.all_issues
            ]
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nJSON report saved to: {output_file}")

def scan_file(file_path: str) -> List[SecurityIssue]:
    """Scan a single Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []
    
    all_issues = []
    
    # AST-based scanning
    try:
        tree = ast.parse(source_code, filename=file_path)
        ast_scanner = FortifyMockScanner(file_path, source_code)
        ast_scanner.visit(tree)
        all_issues.extend(ast_scanner.issues)
    except SyntaxError as e:
        print(f"Syntax error in {file_path}: {e}")
    
    # Regex-based scanning
    regex_scanner = RegexScanner(file_path, source_code)
    all_issues.extend(regex_scanner.scan())
    
    return all_issues

def scan_directory(directory: str, exclude_dirs: List[str] = None) -> List[SecurityIssue]:
    """Scan all Python files in a directory"""
    if exclude_dirs is None:
        exclude_dirs = ['venv', '.venv', 'env', '__pycache__', '.git', 'node_modules']
    
    all_issues = []
    python_files = []
    
    for root, dirs, files in os.walk(directory):
        # Exclude directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                python_files.append(file_path)
    
    print(f"Scanning {len(python_files)} Python files...\n")
    
    for file_path in python_files:
        print(f"Scanning: {file_path}")
        issues = scan_file(file_path)
        all_issues.extend(issues)
    
    return all_issues

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Local Security Scanner - Mock Fortify SCA for Python',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Scan a single file
  python fortify_mock_scanner.py my_script.py
  
  # Scan entire directory
  python fortify_mock_scanner.py /path/to/project
  
  # Generate JSON report
  python fortify_mock_scanner.py my_script.py --json report.json
  
  # Fail build on Critical/High issues
  python fortify_mock_scanner.py my_script.py --fail-on high
        '''
    )
    
    parser.add_argument('path', help='Python file or directory to scan')
    parser.add_argument('--json', help='Output JSON report to file')
    parser.add_argument('--fail-on', choices=['critical', 'high', 'medium', 'low'],
                       help='Fail (exit code 1) if issues of this severity or higher are found')
    parser.add_argument('--exclude', nargs='+', 
                       help='Directories to exclude from scan')
    
    args = parser.parse_args()
    
    # Determine if path is file or directory
    path = Path(args.path)
    
    if not path.exists():
        print(f"Error: Path '{args.path}' does not exist")
        sys.exit(1)
    
    # Scan
    if path.is_file():
        if not path.suffix == '.py':
            print("Error: File must be a Python (.py) file")
            sys.exit(1)
        all_issues = scan_file(str(path))
    else:
        all_issues = scan_directory(str(path), args.exclude)
    
    # Generate report
    reporter = SecurityReportGenerator(all_issues)
    exit_code = reporter.print_console_report()
    
    if args.json:
        reporter.generate_json_report(args.json)
    
    # Check fail-on threshold
    if args.fail_on:
        severity_levels = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        threshold = severity_levels[args.fail_on]
        
        for issue in all_issues:
            issue_level = severity_levels.get(issue.severity.lower(), 4)
            if issue_level <= threshold:
                print(f"\n✗ Build failed: Found {issue.severity} severity issues")
                sys.exit(1)
    
    sys.exit(exit_code if exit_code == 2 else 0)

if __name__ == "__main__":
    main()
