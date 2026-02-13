#!/usr/bin/env python3
"""
CI/CD Pipeline Runner

A comprehensive CI/CD pipeline orchestrator for Python projects.
Run with: python scripts/ci_runner.py --help
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Callable


class StageStatus(Enum):
    PENDING = "⏳"
    RUNNING = "🔄"
    PASSED = "✅"
    FAILED = "❌"
    SKIPPED = "⏭️"


@dataclass
class StageResult:
    name: str
    status: StageStatus
    duration: float = 0.0
    message: str = ""
    output: str = ""


@dataclass
class PipelineConfig:
    project_root: Path = field(default_factory=lambda: Path(__file__).parent.parent)
    reports_dir: Path = field(default_factory=lambda: Path("reports"))
    coverage_threshold: int = 80
    fail_fast: bool = False
    verbose: bool = False
    ci_mode: bool = field(default_factory=lambda: os.getenv("CI", "false").lower() == "true")


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    @classmethod
    def disable(cls):
        cls.HEADER = cls.BLUE = cls.CYAN = cls.GREEN = ""
        cls.YELLOW = cls.RED = cls.BOLD = cls.UNDERLINE = cls.END = ""


class Pipeline:
    """CI/CD Pipeline orchestrator."""
    
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.stages: list[tuple[str, Callable]] = []
        self.results: list[StageResult] = []
        
        # Ensure we're in the project root
        os.chdir(self.config.project_root)
        
        # Create reports directory
        self.config.reports_dir.mkdir(parents=True, exist_ok=True)
        
    def stage(self, name: str):
        """Decorator to register a pipeline stage."""
        def decorator(func: Callable):
            self.stages.append((name, func))
            return func
        return decorator
    
    def run_command(self, cmd: list[str], capture: bool = True, check: bool = True) -> subprocess.CompletedProcess:
        """Run a shell command."""
        if self.config.verbose:
            print(f"{Colors.CYAN}  → {' '.join(cmd)}{Colors.END}")
        
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            check=False
        )
        
        if check and result.returncode != 0:
            if capture:
                print(f"{Colors.RED}{result.stderr or result.stdout}{Colors.END}")
            raise subprocess.CalledProcessError(result.returncode, cmd)
        
        return result
    
    def run_stage(self, name: str, func: Callable) -> StageResult:
        """Execute a single pipeline stage."""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}  {StageStatus.RUNNING.value} Running: {name}{Colors.END}")
        print(f"{Colors.BLUE}{'='*60}{Colors.END}")
        
        start_time = time.time()
        
        try:
            output = func()
            duration = time.time() - start_time
            result = StageResult(
                name=name,
                status=StageStatus.PASSED,
                duration=duration,
                output=output or ""
            )
            print(f"{Colors.GREEN}  {StageStatus.PASSED.value} {name} completed in {duration:.2f}s{Colors.END}")
            
        except subprocess.CalledProcessError as e:
            duration = time.time() - start_time
            result = StageResult(
                name=name,
                status=StageStatus.FAILED,
                duration=duration,
                message=str(e),
                output=e.stdout if hasattr(e, 'stdout') else ""
            )
            print(f"{Colors.RED}  {StageStatus.FAILED.value} {name} failed after {duration:.2f}s{Colors.END}")
            
        except Exception as e:
            duration = time.time() - start_time
            result = StageResult(
                name=name,
                status=StageStatus.FAILED,
                duration=duration,
                message=str(e)
            )
            print(f"{Colors.RED}  {StageStatus.FAILED.value} {name} failed: {e}{Colors.END}")
        
        return result
    
    def run(self, stages_to_run: list[str] | None = None) -> bool:
        """Run the pipeline."""
        print(f"\n{Colors.BOLD}{Colors.HEADER}")
        print("╔══════════════════════════════════════════════════════════╗")
        print("║           🚀 CI/CD PIPELINE STARTING 🚀                  ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")
        print(f"  📁 Project: {self.config.project_root}")
        print(f"  🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  🔧 CI Mode: {self.config.ci_mode}")
        
        stages = self.stages
        if stages_to_run:
            stages = [(n, f) for n, f in self.stages if n in stages_to_run]
        
        all_passed = True
        for name, func in stages:
            result = self.run_stage(name, func)
            self.results.append(result)
            
            if result.status == StageStatus.FAILED:
                all_passed = False
                if self.config.fail_fast:
                    print(f"\n{Colors.RED}Pipeline stopped (fail-fast enabled){Colors.END}")
                    break
        
        self._print_summary()
        self._save_report()
        
        return all_passed
    
    def _print_summary(self):
        """Print pipeline execution summary."""
        print(f"\n{Colors.BOLD}{Colors.HEADER}")
        print("╔══════════════════════════════════════════════════════════╗")
        print("║                   📊 PIPELINE SUMMARY                    ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")
        
        total_duration = sum(r.duration for r in self.results)
        passed = sum(1 for r in self.results if r.status == StageStatus.PASSED)
        failed = sum(1 for r in self.results if r.status == StageStatus.FAILED)
        
        for result in self.results:
            color = Colors.GREEN if result.status == StageStatus.PASSED else Colors.RED
            print(f"  {result.status.value} {result.name:<30} {color}{result.duration:.2f}s{Colors.END}")
        
        print(f"\n  {'─'*50}")
        print(f"  Total Duration: {total_duration:.2f}s")
        print(f"  Stages Passed:  {Colors.GREEN}{passed}{Colors.END}")
        print(f"  Stages Failed:  {Colors.RED}{failed}{Colors.END}")
        
        if failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}  ✨ Pipeline completed successfully! ✨{Colors.END}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}  💥 Pipeline failed! 💥{Colors.END}")
    
    def _save_report(self):
        """Save pipeline report to JSON."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "project": str(self.config.project_root),
            "ci_mode": self.config.ci_mode,
            "stages": [
                {
                    "name": r.name,
                    "status": r.status.name,
                    "duration": r.duration,
                    "message": r.message
                }
                for r in self.results
            ],
            "summary": {
                "total_duration": sum(r.duration for r in self.results),
                "passed": sum(1 for r in self.results if r.status == StageStatus.PASSED),
                "failed": sum(1 for r in self.results if r.status == StageStatus.FAILED)
            }
        }
        
        report_file = self.config.reports_dir / "pipeline-report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n  📄 Report saved to: {report_file}")


# ============================================================================
# PIPELINE STAGES
# ============================================================================

def create_pipeline(config: PipelineConfig) -> Pipeline:
    """Create and configure the CI/CD pipeline."""
    pipeline = Pipeline(config)
    
    @pipeline.stage("install-dependencies")
    def install_dependencies():
        """Install project dependencies."""
        # Check if we need to install
        pipeline.run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install dev dependencies
        if Path("requirements-dev.txt").exists():
            pipeline.run_command([
                sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"
            ])
        
        # Install project in editable mode
        pipeline.run_command([sys.executable, "-m", "pip", "install", "-e", "."])
        
        return "Dependencies installed successfully"
    
    @pipeline.stage("lint-ruff")
    def lint_ruff():
        """Run Ruff linter."""
        reports_dir = config.reports_dir / "lint"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Check for issues
        result = pipeline.run_command(
            [sys.executable, "-m", "ruff", "check", "src/", "tests/", 
             "--output-format=json"],
            check=False
        )
        
        # Save report
        with open(reports_dir / "ruff-report.json", "w") as f:
            f.write(result.stdout)
        
        if result.returncode != 0:
            # Try to fix automatically
            print(f"{Colors.YELLOW}  Attempting auto-fix...{Colors.END}")
            pipeline.run_command(
                [sys.executable, "-m", "ruff", "check", "src/", "tests/", "--fix"],
                check=False
            )
            # Check again
            pipeline.run_command(
                [sys.executable, "-m", "ruff", "check", "src/", "tests/"]
            )
        
        return "Ruff linting passed"
    
    @pipeline.stage("lint-format")
    def lint_format():
        """Check code formatting with Black and isort."""
        # Check Black formatting
        result = pipeline.run_command(
            [sys.executable, "-m", "black", "--check", "--diff", "src/", "tests/"],
            check=False
        )
        
        if result.returncode != 0:
            if not config.ci_mode:
                print(f"{Colors.YELLOW}  Applying Black formatting...{Colors.END}")
                pipeline.run_command(
                    [sys.executable, "-m", "black", "src/", "tests/"]
                )
            else:
                raise subprocess.CalledProcessError(result.returncode, "black")
        
        # Check isort
        result = pipeline.run_command(
            [sys.executable, "-m", "isort", "--check-only", "--diff", "src/", "tests/"],
            check=False
        )
        
        if result.returncode != 0:
            if not config.ci_mode:
                print(f"{Colors.YELLOW}  Applying isort formatting...{Colors.END}")
                pipeline.run_command(
                    [sys.executable, "-m", "isort", "src/", "tests/"]
                )
            else:
                raise subprocess.CalledProcessError(result.returncode, "isort")
        
        return "Code formatting check passed"
    
    @pipeline.stage("test-unit")
    def test_unit():
        """Run unit tests with pytest."""
        reports_dir = config.reports_dir / "test"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        coverage_dir = config.reports_dir / "coverage"
        coverage_dir.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short",
            f"--junitxml={reports_dir}/junit.xml",
            f"--cov=src",
            f"--cov-report=html:{coverage_dir}",
            f"--cov-report=xml:{coverage_dir}/coverage.xml",
            f"--cov-report=term-missing",
            f"--cov-fail-under={config.coverage_threshold}",
        ]
        
        if config.ci_mode:
            cmd.append("--color=yes")
        
        pipeline.run_command(cmd, capture=False)
        
        return f"Tests passed with >={config.coverage_threshold}% coverage"
    
    @pipeline.stage("type-check")
    def type_check():
        """Run mypy type checking."""
        pipeline.run_command(
            [sys.executable, "-m", "mypy", "src/", "--ignore-missing-imports"],
            capture=False
        )
        return "Type checking passed"
    
    @pipeline.stage("security-scan")
    def security_scan():
        """Run security scanning with Bandit."""
        reports_dir = config.reports_dir / "security"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        pipeline.run_command([
            sys.executable, "-m", "bandit",
            "-r", "src/",
            "-f", "json",
            "-o", str(reports_dir / "bandit-report.json"),
            "--severity-level", "medium"
        ], check=False)
        
        # Also run pip-audit for dependency vulnerabilities
        try:
            result = pipeline.run_command(
                [sys.executable, "-m", "pip_audit"],
                check=False
            )
            if result.returncode != 0 and "No known vulnerabilities" not in result.stdout:
                print(f"{Colors.YELLOW}  Warning: Dependency vulnerabilities found{Colors.END}")
        except FileNotFoundError:
            print(f"{Colors.YELLOW}  pip-audit not installed, skipping dependency audit{Colors.END}")
        
        return "Security scan completed"
    
    @pipeline.stage("build-package")
    def build_package():
        """Build Python package."""
        dist_dir = Path("dist")
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
        
        pipeline.run_command([
            sys.executable, "-m", "build"
        ], capture=False)
        
        # List created artifacts
        artifacts = list(dist_dir.glob("*"))
        print(f"\n  📦 Created artifacts:")
        for artifact in artifacts:
            size = artifact.stat().st_size / 1024
            print(f"     - {artifact.name} ({size:.1f} KB)")
        
        return f"Built {len(artifacts)} package(s)"
    
    @pipeline.stage("build-docker")
    def build_docker():
        """Build Docker image."""
        if not Path("docker/Dockerfile").exists():
            print(f"{Colors.YELLOW}  No Dockerfile found, skipping Docker build{Colors.END}")
            return "Skipped - no Dockerfile"
        
        # Get version from pyproject.toml
        version = os.getenv("APP_VERSION", "latest")
        image_name = "myapp"
        
        pipeline.run_command([
            "docker", "build",
            "-t", f"{image_name}:{version}",
            "-t", f"{image_name}:latest",
            "-f", "docker/Dockerfile",
            "."
        ], capture=False)
        
        return f"Built Docker image: {image_name}:{version}"
    
    return pipeline


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="CI/CD Pipeline Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --all                    Run full pipeline
  %(prog)s --lint --test            Run only lint and test stages
  %(prog)s --all --fail-fast        Stop on first failure
  %(prog)s --all --verbose          Show detailed output
        """
    )
    
    parser.add_argument("--all", action="store_true", help="Run all stages")
    parser.add_argument("--lint", action="store_true", help="Run linting stages")
    parser.add_argument("--test", action="store_true", help="Run test stages")
    parser.add_argument("--build", action="store_true", help="Run build stages")
    parser.add_argument("--package", action="store_true", help="Run packaging stages")
    parser.add_argument("--fail-fast", action="store_true", help="Stop on first failure")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    parser.add_argument("--coverage-threshold", type=int, default=80, 
                        help="Minimum coverage percentage (default: 80)")
    
    args = parser.parse_args()
    
    if args.no_color:
        Colors.disable()
    
    config = PipelineConfig(
        fail_fast=args.fail_fast,
        verbose=args.verbose,
        coverage_threshold=args.coverage_threshold
    )
    
    pipeline = create_pipeline(config)
    
    # Determine which stages to run
    stages_to_run = None
    if not args.all:
        stages_to_run = []
        
        # Always install dependencies first
        stages_to_run.append("install-dependencies")
        
        if args.lint:
            stages_to_run.extend(["lint-ruff", "lint-format"])
        if args.test:
            stages_to_run.append("test-unit")
        if args.build:
            stages_to_run.extend(["type-check", "security-scan"])
        if args.package:
            stages_to_run.extend(["build-package", "build-docker"])
        
        if len(stages_to_run) == 1:  # Only install-dependencies
            stages_to_run = None  # Run all
    
    success = pipeline.run(stages_to_run)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
