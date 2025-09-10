#!/usr/bin/env python3
"""
Comprehensive URL Security Validator
Addresses multiple attack vectors beyond basic domain allowlisting
"""

import re
import ipaddress
from urllib.parse import urlparse, unquote, parse_qs
from typing import List, Dict, Set, Optional, Tuple
import logging
from dataclasses import dataclass
from enum import Enum


class ValidationResult(Enum):
    VALID = "valid"
    INVALID_SCHEME = "invalid_scheme"
    INVALID_DOMAIN = "invalid_domain"
    INVALID_PORT = "invalid_port"
    INVALID_PATH = "invalid_path"
    PRIVATE_IP = "private_ip"
    LOCALHOST = "localhost"
    URL_ENCODING_ATTACK = "url_encoding_attack"
    REDIRECT_ATTACK = "redirect_attack"
    PATH_TRAVERSAL = "path_traversal"


@dataclass
class URLValidationConfig:
    """Configuration for URL validation rules"""
    # Domain settings
    allowed_domains: Set[str]
    allow_subdomains: bool = True
    allowed_subdomains: Set[str] = None  # Specific subdomain patterns

    # Protocol settings
    allowed_schemes: Set[str] = None  # Default: {'https'}

    # Port settings
    allowed_ports: Set[int] = None  # Default: {443, 80}
    blocked_ports: Set[int] = None  # Internal/dangerous ports

    # Path settings
    allowed_path_patterns: List[str] = None  # Regex patterns
    blocked_path_patterns: List[str] = None  # Dangerous paths

    # Security settings
    block_private_ips: bool = True
    block_localhost: bool = True
    max_redirects: int = 0  # Block redirect parameters
    decode_url: bool = True  # Decode URL encoding before validation

    # Content validation
    validate_response: bool = False  # Actually fetch and validate response
    max_response_size: int = 1024 * 1024  # 1MB limit


class SecureURLValidator:
    """Comprehensive URL validator addressing multiple security concerns"""

    def __init__(self, config: URLValidationConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Set defaults
        if self.config.allowed_schemes is None:
            self.config.allowed_schemes = {'https'}

        if self.config.allowed_ports is None:
            self.config.allowed_ports = {443, 80}

        if self.config.blocked_ports is None:
            self.config.blocked_ports = {
                22, 23, 25, 53, 110, 143, 993, 995,  # Common service ports
                3306, 5432, 6379, 27017,  # Database ports
                8080, 8443, 9000, 9090,  # Common internal ports
                1433, 1521, 3389,  # Windows/RDP ports
            }

        if self.config.blocked_path_patterns is None:
            self.config.blocked_path_patterns = [
                r'\.\./',  # Path traversal
                r'%2e%2e%2f',  # Encoded path traversal
                r'/etc/',  # System files
                r'/admin',  # Admin interfaces
                r'/internal',  # Internal endpoints
                r'redirect\s*=',  # Redirect parameters
                r'url\s*=',  # URL parameters (open redirect)
            ]

    def validate_url(self, url: str) -> Tuple[ValidationResult, str]:
        """
        Comprehensive URL validation
        Returns: (ValidationResult, error_message)
        """
        try:
            # Step 1: Basic URL parsing
            if not url or not isinstance(url, str):
                return ValidationResult.INVALID_DOMAIN, "URL must be a non-empty string"

            # Step 2: Decode URL if configured
            original_url = url
            if self.config.decode_url:
                url = unquote(url)
                # Check for encoding-based attacks
                if self._detect_encoding_attacks(original_url, url):
                    return ValidationResult.URL_ENCODING_ATTACK, "Suspicious URL encoding detected"

            # Step 3: Parse URL components
            try:
                parsed = urlparse(url)
            except Exception as e:
                return ValidationResult.INVALID_DOMAIN, f"URL parsing failed: {e}"

            # Step 4: Validate scheme
            result = self._validate_scheme(parsed)
            if result[0] != ValidationResult.VALID:
                return result

            # Step 5: Validate domain/host
            result = self._validate_domain(parsed)
            if result[0] != ValidationResult.VALID:
                return result

            # Step 6: Validate port
            result = self._validate_port(parsed)
            if result[0] != ValidationResult.VALID:
                return result

            # Step 7: Validate path
            result = self._validate_path(parsed)
            if result[0] != ValidationResult.VALID:
                return result

            # Step 8: Check for redirect attacks
            result = self._validate_query_parameters(parsed)
            if result[0] != ValidationResult.VALID:
                return result

            # Step 9: Optional response validation
            if self.config.validate_response:
                result = self._validate_response(url)
                if result[0] != ValidationResult.VALID:
                    return result

            return ValidationResult.VALID, "URL is valid"

        except Exception as e:
            self.logger.error(f"URL validation error: {e}")
            return ValidationResult.INVALID_DOMAIN, f"Validation error: {e}"

    def _validate_scheme(self, parsed) -> Tuple[ValidationResult, str]:
        """Validate URL scheme (protocol)"""
        if parsed.scheme not in self.config.allowed_schemes:
            return (ValidationResult.INVALID_SCHEME,
                    f"Scheme '{parsed.scheme}' not in allowed schemes: {self.config.allowed_schemes}")
        return ValidationResult.VALID, ""

    def _validate_domain(self, parsed) -> Tuple[ValidationResult, str]:
        """Validate domain with comprehensive checks"""
        hostname = parsed.hostname
        if not hostname:
            return ValidationResult.INVALID_DOMAIN, "No hostname found"

        # Check for IP addresses
        try:
            ip = ipaddress.ip_address(hostname)

            # Block private IP ranges
            if self.config.block_private_ips and ip.is_private:
                return ValidationResult.PRIVATE_IP, f"Private IP address not allowed: {ip}"

            # Block localhost
            if self.config.block_localhost and ip.is_loopback:
                return ValidationResult.LOCALHOST, f"Localhost not allowed: {ip}"

        except ValueError:
            # Not an IP address, continue with domain validation
            pass

        # Normalize domain for comparison
        domain_lower = hostname.lower()

        # Check localhost names
        if self.config.block_localhost:
            localhost_names = {'localhost', '127.0.0.1', '::1', '0.0.0.0'}
            if domain_lower in localhost_names:
                return ValidationResult.LOCALHOST, f"Localhost not allowed: {hostname}"

        # Check against allowed domains
        domain_allowed = False

        # Exact domain match
        if domain_lower in self.config.allowed_domains:
            domain_allowed = True

        # Subdomain matching if enabled
        elif self.config.allow_subdomains:
            for allowed_domain in self.config.allowed_domains:
                if domain_lower.endswith('.' + allowed_domain.lower()):
                    domain_allowed = True
                    break

        # Check specific subdomain allowlist if configured
        if not domain_allowed and self.config.allowed_subdomains:
            for allowed_subdomain in self.config.allowed_subdomains:
                if re.match(allowed_subdomain, domain_lower):
                    domain_allowed = True
                    break

        if not domain_allowed:
            return (ValidationResult.INVALID_DOMAIN,
                    f"Domain '{hostname}' not in allowed domains")

        return ValidationResult.VALID, ""

    def _validate_port(self, parsed) -> Tuple[ValidationResult, str]:
        """Validate port number"""
        port = parsed.port

        # Use default ports if not specified
        if port is None:
            port = 443 if parsed.scheme == 'https' else 80

        # Check blocked ports
        if port in self.config.blocked_ports:
            return (ValidationResult.INVALID_PORT,
                    f"Port {port} is blocked for security reasons")

        # Check allowed ports
        if port not in self.config.allowed_ports:
            return (ValidationResult.INVALID_PORT,
                    f"Port {port} not in allowed ports: {self.config.allowed_ports}")

        return ValidationResult.VALID, ""

    def _validate_path(self, parsed) -> Tuple[ValidationResult, str]:
        """Validate URL path for traversal and dangerous patterns"""
        path = parsed.path or '/'

        # Check blocked patterns
        for pattern in self.config.blocked_path_patterns:
            if re.search(pattern, path, re.IGNORECASE):
                return (ValidationResult.PATH_TRAVERSAL,
                        f"Path contains blocked pattern: {pattern}")

        # Check allowed patterns if configured
        if self.config.allowed_path_patterns:
            path_allowed = False
            for pattern in self.config.allowed_path_patterns:
                if re.match(pattern, path):
                    path_allowed = True
                    break

            if not path_allowed:
                return (ValidationResult.INVALID_PATH,
                        "Path does not match allowed patterns")

        return ValidationResult.VALID, ""

    def _validate_query_parameters(self, parsed) -> Tuple[ValidationResult, str]:
        """Check query parameters for redirect attacks"""
        if not parsed.query:
            return ValidationResult.VALID, ""

        # Parse query parameters
        query_params = parse_qs(parsed.query, keep_blank_values=True)

        # Check for redirect parameters
        dangerous_params = ['redirect', 'url', 'goto', 'return_url', 'callback']

        for param_name in query_params:
            if param_name.lower() in dangerous_params:
                if self.config.max_redirects == 0:
                    return (ValidationResult.REDIRECT_ATTACK,
                            f"Redirect parameter '{param_name}' not allowed")

        return ValidationResult.VALID, ""

    def _detect_encoding_attacks(self, original: str, decoded: str) -> bool:
        """Detect URL encoding-based attacks"""
        # Check for suspicious encoding patterns
        suspicious_patterns = [
            '%2e%2e',  # ../
            '%2f%2e%2e',  # /..
            '%252e',  # Double encoding
            '%252f',  # Double encoding
        ]

        original_lower = original.lower()
        for pattern in suspicious_patterns:
            if pattern in original_lower:
                return True

        return False

    def _validate_response(self, url: str) -> Tuple[ValidationResult, str]:
        """Optional: Validate actual HTTP response"""
        try:
            import requests

            response = requests.head(url, timeout=5, allow_redirects=False)

            # Check for redirects
            if 300 <= response.status_code < 400:
                return (ValidationResult.REDIRECT_ATTACK,
                        "URL returns redirect response")

            # Check content length
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > self.config.max_response_size:
                return (ValidationResult.INVALID_DOMAIN,
                        "Response too large")

            return ValidationResult.VALID, ""

        except Exception as e:
            return (ValidationResult.INVALID_DOMAIN,
                    f"Failed to validate response: {e}")


# Example usage and test cases
def create_lambda_url_validator() -> SecureURLValidator:
    """Create a validator suitable for Lambda callback URLs"""
    config = URLValidationConfig(
        allowed_domains={
            'api.company.com',
            'webhooks.company.com',
            'trusted-partner.com'
        },
        allow_subdomains=True,
        allowed_schemes={'https'},
        allowed_ports={443},
        block_private_ips=True,
        block_localhost=True,
        allowed_path_patterns=[
            r'^/api/v\d+/webhook/?$',  # Only webhook endpoints
            r'^/callbacks/[a-zA-Z0-9-]+/?$',  # Callback endpoints
        ],
        validate_response=False  # Set to True in production for extra security
    )
    return SecureURLValidator(config)


def validate_lambda_callback_url(url: str) -> bool:
    """
    Secure validation for Lambda callback URLs
    Returns True if URL is safe to use
    """
    validator = create_lambda_url_validator()
    result, message = validator.validate_url(url)

    if result != ValidationResult.VALID:
        logging.warning(f"URL validation failed: {message} for URL: {url}")
        return False

    return True


# Test cases demonstrating security improvements
def test_url_validation():
    """Test cases showing various attack vectors"""
    validator = create_lambda_url_validator()

    test_cases = [
        # Valid URLs
        ("https://api.company.com/api/v1/webhook", True, "Valid webhook URL"),
        ("https://sub.api.company.com/callbacks/user123", True, "Valid subdomain"),

        # Invalid schemes
        ("http://api.company.com/webhook", False, "HTTP not allowed"),
        ("ftp://api.company.com/file", False, "FTP not allowed"),

        # Invalid domains
        ("https://evil.com/webhook", False, "Domain not in allowlist"),
        ("https://api.company.com.evil.com/hook", False, "Domain spoofing"),

        # Port attacks
        ("https://api.company.com:22/webhook", False, "SSH port blocked"),
        ("https://api.company.com:3306/webhook", False, "MySQL port blocked"),

        # Path traversal attacks
        ("https://api.company.com/../../../etc/passwd", False, "Path traversal"),
        ("https://api.company.com/api/v1/webhook/../../admin", False, "Path traversal in valid endpoint"),

        # URL encoding attacks
        ("https://api.company.com/%2e%2e%2fadmin", False, "Encoded path traversal"),

        # Redirect attacks
        ("https://api.company.com/webhook?redirect=https://evil.com", False, "Open redirect"),

        # Localhost attacks
        ("https://127.0.0.1/webhook", False, "Localhost blocked"),
        ("https://localhost/webhook", False, "Localhost name blocked"),

        # Private IP attacks
        ("https://192.168.1.1/webhook", False, "Private IP blocked"),
        ("https://10.0.0.1/webhook", False, "Private IP blocked"),

        # Path validation
        ("https://api.company.com/admin", False, "Admin path not allowed"),
        ("https://api.company.com/random-endpoint", False, "Path not in allowlist"),
    ]

    print("🧪 URL Validation Security Tests")
    print("=" * 50)

    passed = 0
    for url, expected_valid, description in test_cases:
        result, message = validator.validate_url(url)
        actual_valid = (result == ValidationResult.VALID)

        status = "✅ PASS" if actual_valid == expected_valid else "❌ FAIL"
        print(f"{status} {description}")
        print(f"    URL: {url}")
        print(f"    Expected: {'Valid' if expected_valid else 'Invalid'}")
        print(f"    Actual: {result.value} - {message}")
        print()

        if actual_valid == expected_valid:
            passed += 1

    print(f"Results: {passed}/{len(test_cases)} tests passed")


if __name__ == "__main__":
    # Run security tests
    test_url_validation()

    # Example usage in Lambda handler
    print("\n" + "=" * 50)
    print("Example: Secure Lambda Handler")
    print("=" * 50)

    example_code = '''
def lambda_handler(event, context):
    """Secure Lambda handler with comprehensive URL validation"""

    # Get callback URL from request
    callback_url = event.get('callback_url')
    if not callback_url:
        return {'statusCode': 400, 'body': 'Missing callback_url'}

    # Validate URL with comprehensive security checks
    if not validate_lambda_callback_url(callback_url):
        return {
            'statusCode': 400, 
            'body': 'Invalid callback URL - security validation failed'
        }

    # Process webhook data
    payload = {
        'callback_url': callback_url,  # Now safe to use
        'data': event.get('data', {}),
        'timestamp': int(time.time())
    }

    # Send to external service
    response = requests.post(callback_url, json=payload, timeout=30)

    return {'statusCode': 200, 'body': 'Webhook processed successfully'}
    '''

    print(example_code)
