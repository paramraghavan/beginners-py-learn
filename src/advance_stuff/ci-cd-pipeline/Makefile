# ============================================================================
# Python CI/CD Pipeline - Makefile
# ============================================================================
# Run 'make help' to see available commands

.PHONY: help setup install lint format test test-fast test-cov build \
        security type-check package docker clean ci deploy-local \
        deploy-staging deploy-prod

# Colors
BLUE := \033[34m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m
BOLD := \033[1m

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
PROJECT := myapp
SRC_DIR := src
TEST_DIR := tests
REPORTS_DIR := reports

# Default target
.DEFAULT_GOAL := help

# ============================================================================
# Help
# ============================================================================

help: ## Show this help message
	@echo ""
	@echo "$(BOLD)$(BLUE)Python CI/CD Pipeline$(RESET)"
	@echo "$(BOLD)=====================$(RESET)"
	@echo ""
	@echo "$(BOLD)Usage:$(RESET) make [target]"
	@echo ""
	@echo "$(BOLD)Setup:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E "(setup|install)" | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BOLD)Quality:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E "(lint|format|type|security)" | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BOLD)Testing:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E "^test" | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BOLD)Build & Deploy:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E "(build|package|docker|deploy|ci)" | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BOLD)Maintenance:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E "(clean|update)" | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(RESET) %s\n", $$1, $$2}'
	@echo ""

# ============================================================================
# Setup
# ============================================================================

setup: ## Set up development environment (create venv + install deps)
	@echo "$(BOLD)$(BLUE)Setting up development environment...$(RESET)"
	$(PYTHON) -m venv .venv
	@echo "$(GREEN)Virtual environment created at .venv$(RESET)"
	@echo "$(YELLOW)Activate with: source .venv/bin/activate$(RESET)"
	@echo ""
	@echo "Then run: make install"

install: ## Install project and dev dependencies
	@echo "$(BOLD)$(BLUE)Installing dependencies...$(RESET)"
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"
	@echo "$(GREEN)✅ Dependencies installed$(RESET)"

install-prod: ## Install production dependencies only
	$(PIP) install --upgrade pip
	$(PIP) install .

# ============================================================================
# Code Quality
# ============================================================================

lint: ## Run all linters (ruff, black check, isort check)
	@echo "$(BOLD)$(BLUE)Running linters...$(RESET)"
	@echo "\n$(BOLD)Ruff:$(RESET)"
	$(PYTHON) -m ruff check $(SRC_DIR) $(TEST_DIR)
	@echo "\n$(BOLD)Black:$(RESET)"
	$(PYTHON) -m black --check --diff $(SRC_DIR) $(TEST_DIR)
	@echo "\n$(BOLD)isort:$(RESET)"
	$(PYTHON) -m isort --check-only --diff $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)✅ All linting checks passed$(RESET)"

lint-fix: ## Run linters and auto-fix issues
	@echo "$(BOLD)$(BLUE)Fixing linting issues...$(RESET)"
	$(PYTHON) -m ruff check --fix $(SRC_DIR) $(TEST_DIR)
	$(PYTHON) -m black $(SRC_DIR) $(TEST_DIR)
	$(PYTHON) -m isort $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)✅ Linting fixes applied$(RESET)"

format: lint-fix ## Alias for lint-fix

type-check: ## Run mypy type checking
	@echo "$(BOLD)$(BLUE)Running type checks...$(RESET)"
	$(PYTHON) -m mypy $(SRC_DIR) --ignore-missing-imports
	@echo "$(GREEN)✅ Type checking passed$(RESET)"

security: ## Run security scans (bandit + pip-audit)
	@echo "$(BOLD)$(BLUE)Running security scans...$(RESET)"
	@mkdir -p $(REPORTS_DIR)/security
	@echo "\n$(BOLD)Bandit (code security):$(RESET)"
	$(PYTHON) -m bandit -r $(SRC_DIR) -f json -o $(REPORTS_DIR)/security/bandit.json || true
	$(PYTHON) -m bandit -r $(SRC_DIR)
	@echo "\n$(BOLD)pip-audit (dependency vulnerabilities):$(RESET)"
	$(PYTHON) -m pip_audit || true
	@echo "$(GREEN)✅ Security scan complete$(RESET)"

# ============================================================================
# Testing
# ============================================================================

test: ## Run all tests
	@echo "$(BOLD)$(BLUE)Running tests...$(RESET)"
	$(PYTEST) $(TEST_DIR) -v

test-fast: ## Run tests without slow tests
	@echo "$(BOLD)$(BLUE)Running fast tests...$(RESET)"
	$(PYTEST) $(TEST_DIR) -v -m "not slow"

test-cov: ## Run tests with coverage report
	@echo "$(BOLD)$(BLUE)Running tests with coverage...$(RESET)"
	@mkdir -p $(REPORTS_DIR)/coverage $(REPORTS_DIR)/test
	$(PYTEST) $(TEST_DIR) \
		-v \
		--tb=short \
		--junitxml=$(REPORTS_DIR)/test/junit.xml \
		--cov=$(SRC_DIR) \
		--cov-report=html:$(REPORTS_DIR)/coverage \
		--cov-report=xml:$(REPORTS_DIR)/coverage/coverage.xml \
		--cov-report=term-missing \
		--cov-fail-under=80
	@echo ""
	@echo "$(GREEN)✅ Coverage report: $(REPORTS_DIR)/coverage/index.html$(RESET)"

test-watch: ## Run tests in watch mode
	$(PYTEST) $(TEST_DIR) -v --watch

# ============================================================================
# Build
# ============================================================================

build: lint type-check security ## Run all build validations
	@echo "$(GREEN)✅ Build validation complete$(RESET)"

package: ## Build Python package (wheel + sdist)
	@echo "$(BOLD)$(BLUE)Building package...$(RESET)"
	@rm -rf dist/ build/ *.egg-info
	$(PYTHON) -m build
	@echo ""
	@echo "$(GREEN)✅ Package built:$(RESET)"
	@ls -la dist/

docker: ## Build Docker image
	@echo "$(BOLD)$(BLUE)Building Docker image...$(RESET)"
	docker build -t $(PROJECT):latest -f docker/Dockerfile .
	@echo "$(GREEN)✅ Docker image built: $(PROJECT):latest$(RESET)"

docker-run: docker ## Build and run Docker container
	@echo "$(BOLD)$(BLUE)Running Docker container...$(RESET)"
	docker run -p 8000:8000 $(PROJECT):latest

# ============================================================================
# CI/CD
# ============================================================================

ci: ## Run full CI pipeline
	@echo "$(BOLD)$(BLUE)Running full CI pipeline...$(RESET)"
	$(PYTHON) scripts/ci_runner.py --all

ci-quick: ## Run quick CI (lint + test only)
	@echo "$(BOLD)$(BLUE)Running quick CI...$(RESET)"
	$(PYTHON) scripts/ci_runner.py --lint --test

deploy-local: ## Deploy locally
	$(PYTHON) scripts/deploy.py --env local

deploy-staging: ## Deploy to staging
	$(PYTHON) scripts/deploy.py --env staging

deploy-prod: ## Deploy to production (requires confirmation)
	@echo "$(RED)$(BOLD)⚠️  Production deployment requested!$(RESET)"
	@read -p "Type 'yes' to confirm: " confirm && [ "$$confirm" = "yes" ] || exit 1
	$(PYTHON) scripts/deploy.py --env production

# ============================================================================
# Maintenance
# ============================================================================

clean: ## Remove build artifacts and caches
	@echo "$(BOLD)$(BLUE)Cleaning...$(RESET)"
	rm -rf dist/ build/ *.egg-info .eggs/
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/
	rm -rf $(REPORTS_DIR)/
	rm -rf htmlcov/ .coverage coverage.xml
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Clean complete$(RESET)"

clean-all: clean ## Remove everything including venv
	rm -rf .venv/
	@echo "$(GREEN)✅ Full clean complete$(RESET)"

update: ## Update all dependencies
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -e ".[dev]"
	@echo "$(GREEN)✅ Dependencies updated$(RESET)"

# ============================================================================
# Development Helpers
# ============================================================================

run: ## Run the application locally
	$(PYTHON) -m uvicorn myapp.api:app --reload --port 8000

shell: ## Open Python shell with project loaded
	$(PYTHON) -c "from myapp import *; import code; code.interact(local=locals())"

docs: ## Generate documentation
	@echo "Documentation generation not configured yet"

pre-commit: ## Install pre-commit hooks
	pre-commit install
	@echo "$(GREEN)✅ Pre-commit hooks installed$(RESET)"
