# what is BSC - baseline security issue

BSC in the context of Linux or AWS EC2 security typically refers to **Baseline Security Configuration** or **Baseline
Security Controls** - fundamental security measures that should be implemented as a minimum standard.

Here are the key baseline security issues and controls for both:

## Linux Baseline Security Issues:

**Access Control:**

- Weak or default passwords
- Unnecessary user accounts with elevated privileges
- Improper sudo configuration
- Missing SSH key-based authentication

**System Hardening:**

- Unnecessary services running
- Unpatched systems and outdated packages
- Weak file permissions on critical files
- Missing or misconfigured firewall rules

**Monitoring & Logging:**

- Insufficient audit logging
- Missing log monitoring and alerting
- No file integrity monitoring
- Lack of intrusion detection

## AWS EC2 Baseline Security Issues:

**Network Security:**

- Overly permissive security groups (0.0.0.0/0 access)
- Missing VPC configuration
- Unencrypted traffic
- Public subnets for private workloads

**Instance Security:**

- Default or weak EC2 key pairs
- Missing instance metadata service (IMDSv2) enforcement
- Unencrypted EBS volumes
- Missing Systems Manager patch management

**Identity & Access:**

- Overly broad IAM roles attached to instances
- Hardcoded credentials in applications
- Missing MFA requirements
- Inadequate resource tagging for governance

**Monitoring:**

- No CloudTrail logging
- Missing CloudWatch monitoring
- No GuardDuty threat detection
- Insufficient backup strategies

These baseline controls form the foundation of a secure environment and should be addressed before implementing more
advanced security measures.