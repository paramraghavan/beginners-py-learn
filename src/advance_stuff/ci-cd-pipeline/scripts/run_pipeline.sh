#!/bin/bash
#
# CI/CD Pipeline Runner Script
# Usage: ./scripts/run_pipeline.sh [options]
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PYTHON="${PYTHON:-python3}"
VENV_DIR="${PROJECT_ROOT}/.venv"

# Functions
print_header() {
    echo -e "\n${BOLD}${PURPLE}════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${PURPLE}  $1${NC}"
    echo -e "${BOLD}${PURPLE}════════════════════════════════════════════════════════════${NC}\n"
}

print_step() {
    echo -e "${CYAN}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

usage() {
    cat << EOF
${BOLD}CI/CD Pipeline Runner${NC}

${BOLD}Usage:${NC}
    $0 [command] [options]

${BOLD}Commands:${NC}
    setup       Set up development environment
    lint        Run linting checks
    test        Run tests with coverage
    build       Run build validation (type check, security)
    package     Build packages (wheel, docker)
    deploy      Deploy application
    ci          Run full CI pipeline
    clean       Clean build artifacts
    help        Show this help message

${BOLD}Options:${NC}
    --no-venv       Don't use virtual environment
    --verbose       Show detailed output
    --fail-fast     Stop on first failure

${BOLD}Examples:${NC}
    $0 setup                 # Set up environment
    $0 ci                    # Run full CI pipeline
    $0 test --verbose        # Run tests with details
    $0 deploy local          # Deploy locally
    $0 deploy staging        # Deploy to staging

EOF
}

# Check Python version
check_python() {
    if ! command -v "$PYTHON" &> /dev/null; then
        print_error "Python not found. Please install Python 3.10+"
        exit 1
    fi
    
    PY_VERSION=$($PYTHON -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    print_step "Python version: $PY_VERSION"
}

# Setup virtual environment
setup_venv() {
    if [[ "$USE_VENV" == "false" ]]; then
        print_warning "Skipping virtual environment (--no-venv)"
        return
    fi
    
    if [[ ! -d "$VENV_DIR" ]]; then
        print_step "Creating virtual environment..."
        $PYTHON -m venv "$VENV_DIR"
    fi
    
    print_step "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
    
    # Update pip
    pip install --upgrade pip > /dev/null
}

# Setup command
cmd_setup() {
    print_header "🔧 Setting Up Development Environment"
    
    cd "$PROJECT_ROOT"
    check_python
    setup_venv
    
    print_step "Installing dependencies..."
    pip install -e ".[dev]"
    
    print_step "Installing pre-commit hooks..."
    if command -v pre-commit &> /dev/null; then
        pre-commit install
    else
        print_warning "pre-commit not found, skipping hook installation"
    fi
    
    print_success "Environment setup complete!"
    echo -e "\n${CYAN}To activate the virtual environment, run:${NC}"
    echo -e "  source ${VENV_DIR}/bin/activate"
}

# Lint command
cmd_lint() {
    print_header "🔍 Running Linting Checks"
    
    cd "$PROJECT_ROOT"
    setup_venv
    
    local exit_code=0
    
    print_step "Running Ruff..."
    if ruff check src/ tests/; then
        print_success "Ruff passed"
    else
        print_warning "Ruff found issues"
        exit_code=1
    fi
    
    print_step "Checking Black formatting..."
    if black --check --diff src/ tests/ 2>/dev/null; then
        print_success "Black passed"
    else
        print_warning "Black formatting issues found"
        if [[ -z "$CI" ]]; then
            print_step "Auto-formatting with Black..."
            black src/ tests/
        fi
        exit_code=1
    fi
    
    print_step "Checking isort..."
    if isort --check-only src/ tests/ 2>/dev/null; then
        print_success "isort passed"
    else
        print_warning "Import sorting issues found"
        if [[ -z "$CI" ]]; then
            print_step "Auto-sorting imports..."
            isort src/ tests/
        fi
        exit_code=1
    fi
    
    return $exit_code
}

# Test command
cmd_test() {
    print_header "🧪 Running Tests"
    
    cd "$PROJECT_ROOT"
    setup_venv
    
    mkdir -p reports/coverage reports/test
    
    print_step "Running pytest with coverage..."
    pytest tests/ \
        -v \
        --tb=short \
        --junitxml=reports/test/junit.xml \
        --cov=src \
        --cov-report=html:reports/coverage \
        --cov-report=xml:reports/coverage/coverage.xml \
        --cov-report=term-missing \
        --cov-fail-under=80
    
    print_success "Tests passed!"
    echo -e "\n${CYAN}Coverage report: ${PROJECT_ROOT}/reports/coverage/index.html${NC}"
}

# Build command
cmd_build() {
    print_header "🏗️  Running Build Validation"
    
    cd "$PROJECT_ROOT"
    setup_venv
    
    print_step "Running mypy type checking..."
    if mypy src/ --ignore-missing-imports; then
        print_success "Type check passed"
    else
        print_error "Type check failed"
        return 1
    fi
    
    print_step "Running Bandit security scan..."
    mkdir -p reports/security
    if bandit -r src/ -f json -o reports/security/bandit-report.json --severity-level medium 2>/dev/null; then
        print_success "Security scan passed"
    else
        print_warning "Security issues found, check reports/security/bandit-report.json"
    fi
    
    print_step "Checking dependencies for vulnerabilities..."
    if pip-audit 2>/dev/null; then
        print_success "Dependency audit passed"
    else
        print_warning "pip-audit not available or found vulnerabilities"
    fi
}

# Package command
cmd_package() {
    print_header "📦 Building Packages"
    
    cd "$PROJECT_ROOT"
    setup_venv
    
    print_step "Cleaning previous builds..."
    rm -rf dist/ build/ *.egg-info
    
    print_step "Building Python package..."
    python -m build
    
    print_success "Package built successfully!"
    echo -e "\n${CYAN}Artifacts:${NC}"
    ls -la dist/
    
    # Docker build (if Dockerfile exists)
    if [[ -f "docker/Dockerfile" ]]; then
        print_step "Building Docker image..."
        VERSION="${APP_VERSION:-latest}"
        docker build -t myapp:$VERSION -t myapp:latest -f docker/Dockerfile .
        print_success "Docker image built: myapp:$VERSION"
    fi
}

# Deploy command
cmd_deploy() {
    local env="${1:-local}"
    
    print_header "🚀 Deploying to ${env}"
    
    cd "$PROJECT_ROOT"
    
    case "$env" in
        local)
            print_step "Deploying locally..."
            python scripts/deploy.py --env local
            ;;
        staging)
            print_step "Deploying to staging..."
            python scripts/deploy.py --env staging
            ;;
        prod|production)
            print_warning "Production deployment requested!"
            read -p "Are you sure? (yes/no): " confirm
            if [[ "$confirm" == "yes" ]]; then
                python scripts/deploy.py --env production
            else
                print_error "Deployment cancelled"
                return 1
            fi
            ;;
        *)
            print_error "Unknown environment: $env"
            echo "Valid environments: local, staging, prod"
            return 1
            ;;
    esac
}

# Full CI command
cmd_ci() {
    print_header "🔄 Running Full CI Pipeline"
    
    cd "$PROJECT_ROOT"
    
    # Use the Python CI runner for full pipeline
    $PYTHON scripts/ci_runner.py --all ${VERBOSE:+--verbose} ${FAIL_FAST:+--fail-fast}
}

# Clean command
cmd_clean() {
    print_header "🧹 Cleaning Build Artifacts"
    
    cd "$PROJECT_ROOT"
    
    print_step "Removing build directories..."
    rm -rf dist/ build/ *.egg-info .eggs/
    rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/
    rm -rf reports/
    rm -rf htmlcov/ .coverage coverage.xml
    
    print_step "Removing Python cache..."
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type f -name "*.pyo" -delete 2>/dev/null || true
    
    print_success "Clean complete!"
}

# Main
main() {
    # Parse options
    USE_VENV="true"
    VERBOSE=""
    FAIL_FAST=""
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --no-venv)
                USE_VENV="false"
                shift
                ;;
            --verbose|-v)
                VERBOSE="true"
                shift
                ;;
            --fail-fast)
                FAIL_FAST="true"
                shift
                ;;
            help|--help|-h)
                usage
                exit 0
                ;;
            setup|lint|test|build|package|deploy|ci|clean)
                CMD="$1"
                shift
                break
                ;;
            *)
                print_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
    
    # Default to help if no command
    if [[ -z "$CMD" ]]; then
        usage
        exit 0
    fi
    
    # Execute command
    case "$CMD" in
        setup)   cmd_setup ;;
        lint)    cmd_lint ;;
        test)    cmd_test ;;
        build)   cmd_build ;;
        package) cmd_package ;;
        deploy)  cmd_deploy "$@" ;;
        ci)      cmd_ci ;;
        clean)   cmd_clean ;;
    esac
}

main "$@"
