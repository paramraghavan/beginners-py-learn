# ☁️ Cloud & DevOps Guide

> **From Local Development to Production**
>
> Complete guide to containerization, orchestration, cloud platforms, and CI/CD pipelines. Build, deploy, and scale Python applications in production.

---

## Table of Contents

1. [DevOps Overview](#devops-overview)
2. [Docker Fundamentals](#docker-fundamentals)
3. [Docker Best Practices](#docker-best-practices)
4. [Docker Compose](#docker-compose)
5. [Kubernetes Basics](#kubernetes-basics)
6. [Kubernetes Deployments](#kubernetes-deployments)
7. [CI/CD Pipelines](#cicd-pipelines)
8. [GitHub Actions](#github-actions)
9. [AWS Fundamentals](#aws-fundamentals)
10. [AWS Services for Python](#aws-services-for-python)
11. [Environment Management](#environment-management)
12. [Logging & Monitoring](#logging--monitoring)
13. [Infrastructure as Code](#infrastructure-as-code)
14. [Real-World Deployment](#real-world-deployment)

---

## DevOps Overview

### What is DevOps?

DevOps is a set of practices, tools, and cultural philosophies that integrate software development (Dev) and IT operations (Ops).

**Goals:**
- Shorter development cycles
- Frequent deployments
- Reliable releases
- Fast feedback loops
- Automated processes

### DevOps Lifecycle

```
Plan → Code → Build → Test → Release → Deploy → Operate → Monitor → Plan
 ↑                                                                    ↓
 └────────────────────── Feedback Loop ──────────────────────────────┘
```

### Key Principles

1. **Automation** - Reduce manual work, decrease errors
2. **Collaboration** - Dev and Ops working together
3. **Measurement** - Monitor everything, data-driven decisions
4. **Sharing** - Knowledge sharing, blameless culture
5. **Infrastructure as Code** - Version control for infrastructure

### DevOps Tools Stack

```
Version Control: Git, GitHub, GitLab
Build: Jenkins, GitLab CI, GitHub Actions
Container: Docker, Podman
Orchestration: Kubernetes, Docker Swarm
Cloud: AWS, GCP, Azure
Monitoring: Prometheus, ELK Stack, DataDog
IaC: Terraform, CloudFormation, Ansible
```

---

## Docker Fundamentals

### What is Docker?

Docker is a containerization platform that packages applications with dependencies into portable containers.

**Benefits:**
- Consistency (works on laptop, server, cloud)
- Isolation (app dependencies isolated)
- Scalability (easy to spawn containers)
- Resource efficiency (lightweight vs VMs)

### Core Concepts

| Concept | Meaning | Example |
|---------|---------|---------|
| **Image** | Blueprint/template | `python:3.10` |
| **Container** | Running instance of image | Process running your app |
| **Registry** | Image repository | Docker Hub, ECR, GCR |
| **Volume** | Persistent storage | Database files |
| **Network** | Container communication | Service discovery |

### Dockerfile

```dockerfile
# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["python", "main.py"]
```

### Build & Run

```bash
# Build image
docker build -t myapp:1.0 .

# Run container
docker run -d -p 8000:8000 --name myapp myapp:1.0

# View logs
docker logs myapp

# Execute command in container
docker exec -it myapp bash

# Stop container
docker stop myapp

# Remove container
docker rm myapp
```

### Docker Registry

```bash
# Login to Docker Hub
docker login

# Tag image
docker tag myapp:1.0 username/myapp:1.0

# Push to registry
docker push username/myapp:1.0

# Pull from registry
docker pull username/myapp:1.0
```

### Common Commands

```bash
# Images
docker images                    # List images
docker build -t name:tag .      # Build image
docker pull image:tag           # Download image
docker rmi image:tag            # Remove image
docker inspect image:tag        # View image details

# Containers
docker ps                       # Running containers
docker ps -a                    # All containers
docker run -d image:tag         # Run container (detached)
docker run -it image:tag bash   # Interactive shell
docker stop container           # Stop container
docker start container          # Start container
docker rm container             # Remove container
docker logs container           # View logs
docker exec -it container bash  # Execute in container

# Networks
docker network create mynet
docker run --network mynet image

# Volumes
docker volume create myvolume
docker run -v myvolume:/data image
```

---

## Docker Best Practices

### 1. Use Specific Base Image Versions

```dockerfile
# ❌ BAD - Latest may break
FROM python

# ✅ GOOD - Specific version
FROM python:3.10.12-slim
```

### 2. Minimize Layer Count

```dockerfile
# ❌ BAD - Multiple RUN commands
RUN apt-get update
RUN apt-get install -y package1
RUN apt-get install -y package2

# ✅ GOOD - Single RUN command
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*
```

### 3. Leverage Build Cache

```dockerfile
# ✅ GOOD - Order matters (frequently changed files last)
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

### 4. Multi-Stage Builds

```dockerfile
# Build stage
FROM python:3.10 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage (smaller image)
FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "main.py"]
```

### 5. Run as Non-Root User

```dockerfile
# Create non-root user
RUN useradd -m appuser
USER appuser

# Run application
CMD ["python", "main.py"]
```

### 6. Use .dockerignore

```
.git
.gitignore
__pycache__
*.pyc
.venv
.env
node_modules
.DS_Store
```

### 7. Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

### 8. Small Image Size

```dockerfile
# ✅ GOOD - 150MB
FROM python:3.10-slim

# ❌ BAD - 900MB
FROM python:3.10
```

### 9. Environment Variables

```dockerfile
# Set defaults
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Can be overridden
ENV APP_ENV=production
```

### 10. Logging

```dockerfile
# Python logs to stdout/stderr
# Docker captures automatically
CMD ["python", "-u", "main.py"]
```

---

## Docker Compose

### docker-compose.yml

```yaml
version: '3.9'

services:
  # Python application
  app:
    build: .
    container_name: myapp
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
    networks:
      - mynetwork
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s

  # PostgreSQL database
  db:
    image: postgres:15-alpine
    container_name: myapp_db
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - mynetwork
    restart: unless-stopped

  # Redis cache
  cache:
    image: redis:7-alpine
    container_name: myapp_cache
    networks:
      - mynetwork
    restart: unless-stopped

  # Nginx reverse proxy
  nginx:
    image: nginx:alpine
    container_name: myapp_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - app
    networks:
      - mynetwork
    restart: unless-stopped

volumes:
  db_data:

networks:
  mynetwork:
    driver: bridge
```

### Docker Compose Commands

```bash
# Build and start services
docker-compose up -d

# View running services
docker-compose ps

# View logs
docker-compose logs -f app

# Execute command
docker-compose exec app bash

# Stop services
docker-compose down

# Remove volumes too
docker-compose down -v

# Rebuild
docker-compose build --no-cache
```

---

## Kubernetes Basics

### What is Kubernetes?

Kubernetes (K8s) is an open-source container orchestration platform that automates deployment, scaling, and management of containerized applications.

**Key Features:**
- Automated deployment & scaling
- Self-healing (restart failed containers)
- Load balancing
- Rolling updates
- Resource management
- Storage orchestration

### Kubernetes Architecture

```
Master Node (Control Plane)
├── API Server (REST API)
├── Scheduler (assign pods to nodes)
├── Controller Manager (maintain desired state)
└── etcd (cluster database)

Worker Nodes (Compute)
├── Pod 1 (app container)
├── Pod 2 (app container)
├── Kubelet (node agent)
└── Container Runtime (Docker)
```

### Core Concepts

| Concept | Purpose | Example |
|---------|---------|---------|
| **Pod** | Smallest unit, wraps container | Single Python app instance |
| **Deployment** | Manages pod replicas | "Run 3 copies of my app" |
| **Service** | Network access to pods | LoadBalancer, ClusterIP |
| **ConfigMap** | Configuration data | Database connection string |
| **Secret** | Sensitive data | API keys, passwords |
| **Volume** | Persistent storage | Database files |
| **Namespace** | Logical isolation | dev, staging, prod |

### Pod Definition

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: app
    image: myapp:1.0
    ports:
    - containerPort: 8000
    env:
    - name: DATABASE_URL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: database_url
    - name: API_KEY
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: api_key
    resources:
      requests:
        memory: "256Mi"
        cpu: "250m"
      limits:
        memory: "512Mi"
        cpu: "500m"
```

---

## Kubernetes Deployments

### Deployment Definition

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
  labels:
    app: myapp
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:1.0
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8000
        env:
        - name: ENVIRONMENT
          value: "production"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Service Definition

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

### ConfigMap & Secrets

```yaml
# ConfigMap (non-sensitive config)
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database_url: "postgresql://user:pass@db:5432/mydb"
  log_level: "INFO"
  max_connections: "100"

---
# Secret (sensitive data - base64 encoded)
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  api_key: YWJjZDEyMzQ=  # base64 encoded
  db_password: cGFzc3dvcmQxMjM=
```

### kubectl Commands

```bash
# Cluster info
kubectl cluster-info
kubectl get nodes
kubectl get namespaces

# Deployments
kubectl create deployment myapp --image=myapp:1.0
kubectl get deployments
kubectl get pods
kubectl describe pod pod-name
kubectl logs pod-name
kubectl logs pod-name --previous  # Previous crashed instance

# Scaling
kubectl scale deployment myapp --replicas=5

# Rolling update
kubectl set image deployment/myapp app=myapp:2.0 --record
kubectl rollout status deployment/myapp
kubectl rollout history deployment/myapp
kubectl rollout undo deployment/myapp

# Apply manifests
kubectl apply -f deployment.yaml
kubectl delete -f deployment.yaml

# Debugging
kubectl exec -it pod-name bash
kubectl port-forward pod-name 8000:8000
kubectl top nodes
kubectl top pods
```

---

## CI/CD Pipelines

### What is CI/CD?

**Continuous Integration (CI):**
- Automated testing on every commit
- Detect integration issues early
- Build artifacts automatically

**Continuous Deployment (CD):**
- Automated deployment to production
- No manual deployment steps
- Fast feedback loop

### Pipeline Stages

```
Code Push → Checkout → Build → Test → Deploy → Monitor
   ↓          ↓        ↓      ↓      ↓        ↓
GitHub    Fetch Repo Build App Run Tests Deploy Staging Monitor Logs
```

### Basic Pipeline

```yaml
# Example: GitHub Actions, GitLab CI, Jenkins similar

trigger:
  - push
  - pull_request

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # 1. Checkout code
      - uses: actions/checkout@v3

      # 2. Setup Python
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      # 3. Install dependencies
      - run: pip install -r requirements.txt

      # 4. Lint
      - run: flake8 src/

      # 5. Test
      - run: pytest tests/ --cov

      # 6. Build Docker image
      - run: docker build -t myapp:${{ github.sha }} .

      # 7. Push to registry
      - run: docker push myapp:${{ github.sha }}

      # 8. Deploy
      - run: kubectl set image deployment/myapp app=myapp:${{ github.sha }}
```

---

## GitHub Actions

### What is GitHub Actions?

GitHub Actions is a CI/CD service built into GitHub that runs workflows on events (push, PR, schedule).

### Workflow File

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          cache: 'pip'

      - run: pip install -r requirements.txt

      - name: Lint with flake8
        run: |
          flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 src/ --count --exit-zero --max-complexity=10

      - name: Type check with mypy
        run: mypy src/

      - name: Test with pytest
        run: pytest tests/ --cov=src --cov-report=xml
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v3

      - uses: docker/setup-buildx-action@v2

      - uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          cache-from: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:buildcache
          cache-to: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:buildcache,mode=max

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Kubernetes
        run: |
          kubectl config set-cluster my-cluster --server=${{ secrets.KUBE_SERVER }}
          kubectl config set-credentials my-user --token=${{ secrets.KUBE_TOKEN }}
          kubectl config set-context my-context --cluster=my-cluster --user=my-user
          kubectl config use-context my-context
          kubectl set image deployment/myapp app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
```

### Common Actions

```yaml
# Checkout code
- uses: actions/checkout@v3

# Setup Python
- uses: actions/setup-python@v4
  with:
    python-version: '3.10'

# Cache dependencies
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

# Secrets
- run: echo ${{ secrets.SECRET_NAME }}

# Context variables
- run: echo "Branch: ${{ github.ref }}"
- run: echo "SHA: ${{ github.sha }}"
- run: echo "Actor: ${{ github.actor }}"
```

---

## AWS Fundamentals

### AWS Services Overview

```
Compute:
├── EC2 (Virtual machines)
├── Lambda (Serverless functions)
├── ECS (Container orchestration)
└── AppRunner (Container hosting)

Storage:
├── S3 (Object storage)
├── EBS (Block storage)
├── EFS (File storage)
└── Glacier (Archive)

Database:
├── RDS (Relational databases)
├── DynamoDB (NoSQL)
├── ElastiCache (Caching)
└── Neptune (Graph)

Networking:
├── VPC (Virtual network)
├── ALB/NLB (Load balancers)
├── CloudFront (CDN)
└── Route 53 (DNS)

Developer Tools:
├── CodeBuild (Build service)
├── CodePipeline (CI/CD)
├── CodeDeploy (Deployment)
└── CloudFormation (IaC)
```

### EC2 Instance

```python
import boto3

ec2 = boto3.client('ec2')

# Launch instance
response = ec2.run_instances(
    ImageId='ami-0c55b159cbfafe1f0',  # Amazon Linux 2
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='my-key-pair',
    SecurityGroups=['my-security-group']
)

instance_id = response['Instances'][0]['InstanceId']
print(f"Launched instance: {instance_id}")

# Stop instance
ec2.stop_instances(InstanceIds=[instance_id])

# Terminate instance
ec2.terminate_instances(InstanceIds=[instance_id])
```

### S3 Operations

```python
import boto3

s3 = boto3.client('s3')

# Upload file
s3.upload_file('local_file.txt', 'my-bucket', 's3_key.txt')

# Download file
s3.download_file('my-bucket', 's3_key.txt', 'downloaded.txt')

# List objects
response = s3.list_objects_v2(Bucket='my-bucket')
for obj in response.get('Contents', []):
    print(obj['Key'])

# Delete object
s3.delete_object(Bucket='my-bucket', Key='s3_key.txt')

# Create bucket
s3.create_bucket(Bucket='my-new-bucket')
```

### Lambda Function

```python
# lambda_function.py
def lambda_handler(event, context):
    """
    event: Input data
    context: Runtime information
    """

    body = event.get('body', {})
    name = body.get('name', 'World')

    return {
        'statusCode': 200,
        'body': f'Hello, {name}!'
    }
```

```yaml
# serverless.yml (Serverless Framework)
service: my-api

provider:
  name: aws
  runtime: python3.10
  region: us-east-1

functions:
  hello:
    handler: handler.lambda_handler
    events:
      - http:
          path: hello
          method: post
```

---

## AWS Services for Python

### RDS (Relational Database Service)

```python
import boto3
import pymysql

rds = boto3.client('rds')

# Create database
rds.create_db_instance(
    DBInstanceIdentifier='mydb',
    DBInstanceClass='db.t3.micro',
    Engine='mysql',
    MasterUsername='admin',
    MasterUserPassword='password123',
    AllocatedStorage=20
)

# Connect to database
connection = pymysql.connect(
    host='mydb.xxxxxxxx.us-east-1.rds.amazonaws.com',
    user='admin',
    password='password123',
    database='mydb'
)
```

### DynamoDB

```python
import boto3

dynamodb = boto3.client('dynamodb')

# Put item
dynamodb.put_item(
    TableName='Users',
    Item={
        'id': {'S': '123'},
        'name': {'S': 'Alice'},
        'email': {'S': 'alice@example.com'}
    }
)

# Get item
response = dynamodb.get_item(
    TableName='Users',
    Key={'id': {'S': '123'}}
)
print(response['Item'])

# Query
response = dynamodb.query(
    TableName='Users',
    KeyConditionExpression='id = :id',
    ExpressionAttributeValues={':id': {'S': '123'}}
)
```

### SQS (Simple Queue Service)

```python
import boto3
import json

sqs = boto3.client('sqs')

queue_url = 'https://sqs.region.amazonaws.com/account/queue-name'

# Send message
sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=json.dumps({'key': 'value'})
)

# Receive message
response = sqs.receive_message(QueueUrl=queue_url)
for message in response.get('Messages', []):
    print(message['Body'])
    # Delete after processing
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=message['ReceiptHandle']
    )
```

### CloudWatch (Monitoring)

```python
import boto3

cloudwatch = boto3.client('cloudwatch')

# Put metric
cloudwatch.put_metric_data(
    Namespace='MyApp',
    MetricData=[
        {
            'MetricName': 'ProcessedRecords',
            'Value': 100,
            'Unit': 'Count'
        }
    ]
)

# Get metric statistics
response = cloudwatch.get_metric_statistics(
    Namespace='MyApp',
    MetricName='ProcessedRecords',
    StartTime='2024-01-01',
    EndTime='2024-01-31',
    Period=3600,  # 1 hour
    Statistics=['Sum', 'Average']
)
```

---

## Environment Management

### Environment Variables

```python
import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# Access variables
DATABASE_URL = os.getenv('DATABASE_URL')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
PORT = int(os.getenv('PORT', 8000))

# With defaults
API_KEY = os.getenv('API_KEY', 'default-key')
```

### .env File

```
# Development
DATABASE_URL=sqlite:///dev.db
REDIS_URL=redis://localhost:6379
DEBUG=True
SECRET_KEY=dev-secret-key
```

### Configuration Management

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///dev.db"

    # Redis
    redis_url: str = "redis://localhost:6379"

    # Security
    secret_key: str
    debug: bool = False

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()
```

### Secrets Management

**AWS Secrets Manager:**
```python
import boto3

secrets = boto3.client('secretsmanager')

response = secrets.get_secret_value(SecretId='db-password')
password = response['SecretString']
```

**HashiCorp Vault:**
```python
import hvac

client = hvac.Client(url='http://vault:8200')
secret = client.secrets.kv.read_secret_version(path='secret/database')
password = secret['data']['data']['password']
```

---

## Logging & Monitoring

### Structured Logging

```python
import logging
import json
import sys

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }

        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_data)

# Setup logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Usage
logger.info("Application started")
logger.warning("CPU usage high", extra={'cpu': 85})
logger.error("Database connection failed", exc_info=True)
```

### Health Checks

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/health")
async def health_check():
    """Liveness probe - is app running?"""
    return {"status": "ok"}

@app.get("/ready")
async def readiness_check():
    """Readiness probe - can app handle traffic?"""
    # Check database
    if not await check_database():
        raise HTTPException(status_code=503)

    # Check cache
    if not await check_redis():
        raise HTTPException(status_code=503)

    return {"status": "ready"}

async def check_database():
    try:
        async with db.connection() as conn:
            await conn.execute("SELECT 1")
        return True
    except:
        return False
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, start_http_server
import time

# Define metrics
request_count = Counter(
    'app_requests_total',
    'Total requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'app_request_duration_seconds',
    'Request duration',
    ['method', 'endpoint']
)

# Middleware
async def prometheus_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    request_duration.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    return response

# Start metrics server
start_http_server(8001)
```

---

## Infrastructure as Code

### Terraform

```hcl
# main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "main-vpc"
  }
}

# Subnet
resource "aws_subnet" "main" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "main-subnet"
  }
}

# RDS Instance
resource "aws_db_instance" "main" {
  identifier     = "myapp-db"
  engine         = "postgres"
  engine_version = "15.3"
  instance_class = "db.t3.micro"

  db_name  = "myapp"
  username = "postgres"
  password = random_password.db_password.result

  skip_final_snapshot = true

  tags = {
    Name = "myapp-database"
  }
}

# RDS Password
resource "random_password" "db_password" {
  length  = 16
  special = true
}

# Output
output "db_endpoint" {
  value       = aws_db_instance.main.endpoint
  description = "Database endpoint"
}

# variables.tf
variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}
```

### CloudFormation

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'CloudFormation template for Python application'

Resources:
  MyRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: 'sts:AssumeRole'

  MyInstanceProfile:
    Type: AWS::IAM::InstanceProfile
    Properties:
      Roles:
        - !Ref MyRole

  MySecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for app
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 8000
          ToPort: 8000
          CidrIp: 0.0.0.0/0

  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-0c55b159cbfafe1f0
      InstanceType: t2.micro
      IamInstanceProfile: !Ref MyInstanceProfile
      SecurityGroupIds:
        - !Ref MySecurityGroup
      UserData:
        Fn::Base64: |
          #!/bin/bash
          yum update -y
          yum install -y python3 python3-pip
          pip3 install fastapi uvicorn
```

---

## Real-World Deployment

### Complete Stack

```yaml
# docker-compose.yml (Local)
version: '3.9'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/myapp
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
    volumes:
      - ./src:/app/src

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  cache:
    image: redis:7-alpine

volumes:
  postgres_data:
```

```yaml
# kubernetes/deployment.yaml (Production)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

### Deployment Checklist

- [ ] Code in version control (Git)
- [ ] Tests passing (unit, integration)
- [ ] Code review completed
- [ ] Dockerfile optimized
- [ ] Image pushed to registry
- [ ] Kubernetes manifests created
- [ ] Secrets configured
- [ ] Health checks defined
- [ ] Monitoring setup
- [ ] Logging configured
- [ ] Database migrations ready
- [ ] Rollback plan documented
- [ ] Team notified
- [ ] Post-deployment tests run

---

## Best Practices

### Docker

✅ Use specific base image versions
✅ Multi-stage builds for smaller images
✅ Run as non-root user
✅ Use health checks
✅ Minimize layers
✅ Leverage build cache

### Kubernetes

✅ Resource requests & limits
✅ Health checks (liveness & readiness)
✅ Rolling updates
✅ Namespaces for isolation
✅ Network policies
✅ RBAC for security

### CI/CD

✅ Fail fast (lint before tests)
✅ Run tests in parallel
✅ Use caching
✅ Deploy to staging first
✅ Automated rollback
✅ Post-deployment tests

### AWS

✅ Use IAM roles (not credentials)
✅ Enable MFA on root account
✅ VPC for isolation
✅ Encryption for data
✅ CloudWatch for monitoring
✅ Cost monitoring

---

## Resources

**Docker:**
- Official Docker Documentation
- Play with Docker (free environment)
- Docker Best Practices Guide

**Kubernetes:**
- Official Kubernetes Documentation
- Kubernetes in Action (book)
- Play with Kubernetes

**CI/CD:**
- GitHub Actions Documentation
- GitLab CI Documentation
- Jenkins Documentation

**AWS:**
- AWS Whitepapers
- AWS Well-Architected Framework
- AWS Python Boto3 Documentation

---

**Last Updated:** May 2026 | **Version:** 1.0

Related resources:
- [Quick Reference Cards](quick-reference-cards.md) - Docker, AWS, Git commands
- [Python Study Guide](python-study-guide.md) - Python fundamentals
- [Main Handbook](PYTHON_HANDBOOK.md) - Complete overview
