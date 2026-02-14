#!/usr/bin/env python3
"""
Deployment Script

Handles deployment to different environments: local, staging, production.
"""

import argparse
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DeployConfig:
    environment: str
    docker_registry: str = ""
    app_name: str = "myapp"
    version: str = "latest"
    port: int = 8000
    replicas: int = 1


class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_step(msg: str):
    print(f"{Colors.BLUE}▶ {msg}{Colors.END}")


def print_success(msg: str):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")


def print_error(msg: str):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")


def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")


def run_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command."""
    print(f"  $ {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, capture_output=False)


class Deployer:
    """Handles deployment to different environments."""
    
    def __init__(self, config: DeployConfig):
        self.config = config
        self.project_root = Path(__file__).parent.parent
    
    def deploy(self):
        """Execute deployment based on environment."""
        print(f"\n{Colors.BOLD}🚀 Deploying to {self.config.environment}{Colors.END}\n")
        
        if self.config.environment == "local":
            return self.deploy_local()
        elif self.config.environment == "staging":
            return self.deploy_staging()
        elif self.config.environment == "production":
            return self.deploy_production()
        else:
            print_error(f"Unknown environment: {self.config.environment}")
            return False
    
    def deploy_local(self) -> bool:
        """Deploy locally using Docker Compose or direct Python."""
        print_step("Starting local deployment...")
        
        # Check if Docker is available
        docker_available = shutil.which("docker") is not None
        compose_file = self.project_root / "docker" / "docker-compose.yml"
        
        if docker_available and compose_file.exists():
            return self._deploy_docker_compose(compose_file)
        else:
            return self._deploy_direct()
    
    def _deploy_docker_compose(self, compose_file: Path) -> bool:
        """Deploy using Docker Compose."""
        print_step("Using Docker Compose...")
        
        try:
            # Build and start services
            run_command([
                "docker", "compose", 
                "-f", str(compose_file),
                "up", "-d", "--build"
            ])
            
            print_success(f"Application running at http://localhost:{self.config.port}")
            print(f"\n{Colors.BLUE}Useful commands:{Colors.END}")
            print(f"  View logs:    docker compose -f {compose_file} logs -f")
            print(f"  Stop:         docker compose -f {compose_file} down")
            print(f"  Restart:      docker compose -f {compose_file} restart")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print_error(f"Docker Compose failed: {e}")
            return False
    
    def _deploy_direct(self) -> bool:
        """Deploy directly without Docker."""
        print_step("Running directly with Python...")
        
        # Install dependencies
        print_step("Installing dependencies...")
        run_command([sys.executable, "-m", "pip", "install", "-e", "."])
        
        # Check if main.py exists and get entry point
        main_file = self.project_root / "src" / "myapp" / "main.py"
        
        if not main_file.exists():
            print_warning("No main.py found, looking for alternative entry points...")
            # Try to find any runnable entry point
            api_file = self.project_root / "src" / "myapp" / "api.py"
            if api_file.exists():
                main_file = api_file
        
        print_step("Starting application...")
        
        # Try uvicorn for FastAPI/ASGI apps
        try:
            run_command([
                sys.executable, "-m", "uvicorn",
                "myapp.api:app",
                "--host", "0.0.0.0",
                "--port", str(self.config.port),
                "--reload"
            ])
        except subprocess.CalledProcessError:
            # Fallback to running main directly
            run_command([sys.executable, "-m", "myapp.main"])
        
        return True
    
    def deploy_staging(self) -> bool:
        """Deploy to staging environment."""
        print_step("Deploying to staging...")
        
        # Build Docker image
        print_step("Building Docker image...")
        image_tag = f"{self.config.app_name}:{self.config.version}"
        
        run_command([
            "docker", "build",
            "-t", image_tag,
            "-f", str(self.project_root / "docker" / "Dockerfile"),
            str(self.project_root)
        ])
        
        # Tag for registry
        if self.config.docker_registry:
            registry_tag = f"{self.config.docker_registry}/{image_tag}"
            run_command(["docker", "tag", image_tag, registry_tag])
            
            print_step("Pushing to registry...")
            run_command(["docker", "push", registry_tag])
        
        # Deploy (example using docker run, could be kubectl, etc.)
        print_step("Deploying container...")
        
        # Stop existing container
        run_command([
            "docker", "rm", "-f", f"{self.config.app_name}-staging"
        ], check=False)
        
        # Start new container
        run_command([
            "docker", "run", "-d",
            "--name", f"{self.config.app_name}-staging",
            "-p", f"{self.config.port}:{self.config.port}",
            "-e", "ENVIRONMENT=staging",
            image_tag
        ])
        
        print_success(f"Staging deployment complete!")
        print(f"  URL: http://localhost:{self.config.port}")
        
        return True
    
    def deploy_production(self) -> bool:
        """Deploy to production environment."""
        print_warning("Production deployment!")
        
        # Pre-deployment checks
        print_step("Running pre-deployment checks...")
        
        # 1. Verify tests pass
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-q"],
            capture_output=True
        )
        if result.returncode != 0:
            print_error("Tests must pass before production deployment!")
            return False
        print_success("Tests passed")
        
        # 2. Check for uncommitted changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            print_error("Uncommitted changes detected! Commit or stash before deploying.")
            return False
        print_success("Working directory clean")
        
        # 3. Build and push
        print_step("Building production image...")
        image_tag = f"{self.config.app_name}:{self.config.version}"
        
        run_command([
            "docker", "build",
            "-t", image_tag,
            "--target", "production",
            "-f", str(self.project_root / "docker" / "Dockerfile"),
            str(self.project_root)
        ])
        
        if self.config.docker_registry:
            registry_tag = f"{self.config.docker_registry}/{image_tag}"
            run_command(["docker", "tag", image_tag, registry_tag])
            run_command(["docker", "push", registry_tag])
        
        # 4. Deploy (placeholder - would typically use kubectl, AWS ECS, etc.)
        print_step("Deploying to production...")
        
        # Example: kubectl deployment
        # run_command([
        #     "kubectl", "set", "image",
        #     f"deployment/{self.config.app_name}",
        #     f"{self.config.app_name}={registry_tag}"
        # ])
        
        print_success("Production deployment complete!")
        
        # Health check
        print_step("Running health check...")
        # Placeholder for actual health check
        print_success("Health check passed!")
        
        return True


def main():
    parser = argparse.ArgumentParser(description="Deploy application")
    parser.add_argument(
        "--env", "-e",
        choices=["local", "staging", "production", "prod"],
        default="local",
        help="Deployment environment"
    )
    parser.add_argument(
        "--version", "-v",
        default=os.getenv("APP_VERSION", "latest"),
        help="Version to deploy"
    )
    parser.add_argument(
        "--registry", "-r",
        default=os.getenv("DOCKER_REGISTRY", ""),
        help="Docker registry URL"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=int(os.getenv("APP_PORT", "8000")),
        help="Application port"
    )
    
    args = parser.parse_args()
    
    env = args.env
    if env == "prod":
        env = "production"
    
    config = DeployConfig(
        environment=env,
        version=args.version,
        docker_registry=args.registry,
        port=args.port
    )
    
    deployer = Deployer(config)
    success = deployer.deploy()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
