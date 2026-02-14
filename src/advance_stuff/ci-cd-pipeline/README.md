# Python CI/CD Pipeline

A complete, production-ready CI/CD pipeline that you can run locally or integrate with GitHub Actions.

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CI/CD PIPELINE STAGES                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────────┐   │
│  │  LINT   │──▶│  TEST   │──▶│  BUILD  │──▶│ PACKAGE │──▶│   DEPLOY    │   │
│  └─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────────┘   │
│       │             │             │             │               │          │
│       ▼             ▼             ▼             ▼               ▼          │
│   - Ruff        - Pytest     - Validate    - Docker        - Local        │
│   - Black       - Coverage   - Type Check  - Wheel/Tar     - Staging      │
│   - isort       - Reports    - Security    - Push Image    - Production   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.10+
- Docker (optional, for containerized deployment)
- Make (optional, but recommended)

### Run Locally

```bash
# Clone and enter directory
cd python-cicd-pipeline

# Option 1: Using Make (recommended)
make setup      # Install dependencies
make ci         # Run full CI pipeline
make deploy     # Deploy locally

# Option 2: Using the runner script
./scripts/run_pipeline.sh

# Option 3: Step by step
pip install -e ".[dev]"
python scripts/ci_runner.py --all
```

## Pipeline Stages

### 1. **Lint** - Code Quality Checks

| Tool | Purpose |
|------|---------|
| Ruff | Fast Python linter (replaces flake8, pylint) |
| Black | Code formatter |
| isort | Import sorter |

```bash
make lint
# or
python scripts/ci_runner.py --lint
```

### 2. **Test** - Automated Testing

| Component | Description |
|-----------|-------------|
| pytest | Test framework |
| pytest-cov | Coverage reporting |
| pytest-xdist | Parallel test execution |

```bash
make test
# or
python scripts/ci_runner.py --test
```

### 3. **Build** - Validation & Security

| Check | Tool |
|-------|------|
| Type checking | mypy |
| Security scan | bandit |
| Dependency audit | pip-audit |

```bash
make build
# or
python scripts/ci_runner.py --build
```

### 4. **Package** - Create Artifacts

Creates distributable packages:
- Python wheel (`.whl`)
- Source distribution (`.tar.gz`)
- Docker image

```bash
make package
# or
python scripts/ci_runner.py --package
```

### 5. **Deploy** - Ship It!

Supports multiple deployment targets:

```bash
make deploy-local      # Local deployment
make deploy-staging    # Staging environment
make deploy-prod       # Production (requires confirmation)
```

## Project Structure

```
python-cicd-pipeline/
├── src/
│   └── myapp/              # Your application code
│       ├── __init__.py
│       ├── main.py
│       ├── api.py
│       └── utils.py
├── tests/                  # Test files
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_api.py
│   └── conftest.py
├── scripts/
│   ├── ci_runner.py        # Main CI/CD orchestrator
│   ├── run_pipeline.sh     # Shell script runner
│   └── deploy.py           # Deployment script
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions workflow
├── docker/
│   ├── Dockerfile          # Production image
│   └── Dockerfile.dev      # Development image
├── Makefile                # Make targets
├── pyproject.toml          # Project configuration
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
└── README.md               # This file
```

## Configuration

### pyproject.toml

All tool configurations are centralized in `pyproject.toml`:

- Project metadata
- Ruff settings
- Black settings
- pytest settings
- mypy settings
- Coverage settings

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CI` | Running in CI environment | `false` |
| `DEPLOY_ENV` | Deployment target | `local` |
| `DOCKER_REGISTRY` | Docker registry URL | `localhost:5000` |
| `APP_VERSION` | Application version | from pyproject.toml |

## GitHub Actions Integration

The included `.github/workflows/ci.yml` provides:

- Triggered on push/PR to main
- Matrix testing (Python 3.10, 3.11, 3.12)
- Caching for fast builds
- Artifact upload
- Deployment gates

## Reports & Artifacts

After running the pipeline, find reports in:

```
reports/
├── coverage/
│   ├── index.html          # Coverage HTML report
│   └── coverage.xml        # Coverage XML (for CI)
├── lint/
│   └── ruff-report.json    # Linting results
├── security/
│   └── bandit-report.json  # Security scan results
└── test/
    └── junit.xml           # Test results (JUnit format)
```

## Customization

### Adding New Stages

Edit `scripts/ci_runner.py` to add custom stages:

```python
@pipeline.stage("my-stage")
def my_custom_stage():
    # Your custom logic
    pass
```

### Changing Tools

Swap tools by editing `pyproject.toml` and updating the corresponding stage in `ci_runner.py`.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `make: command not found` | Use `./scripts/run_pipeline.sh` instead |
| Permission denied on scripts | Run `chmod +x scripts/*.sh` |
| Docker build fails | Ensure Docker daemon is running |
| Tests fail with import errors | Run `pip install -e .` first |

## Sample ETL Application

This project includes a complete **ETL (Extract, Transform, Load)** application that demonstrates the CI/CD pipeline with real business logic.

### ETL Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  EXTRACT    │────▶│  TRANSFORM  │────▶│    LOAD     │
├─────────────┤     ├─────────────┤     ├─────────────┤
│ • JSON      │     │ • Clean     │     │ • JSON      │
│ • CSV       │     │ • Filter    │     │ • JSONL     │
│ • API       │     │ • Rename    │     │ • CSV       │
│ • In-Memory │     │ • Compute   │     │ • In-Memory │
└─────────────┘     │ • Validate  │     └─────────────┘
                    └─────────────┘
```

### Quick ETL Examples

```bash
# Run example ETL pipelines
python -m myapp.etl.examples

# Use the CLI
python -m myapp.etl.cli -i data/sample_employees.json -o output/employees.csv --output-format csv

# Transform orders with calculations
python -m myapp.etl.cli \
  -i data/sample_orders.csv \
  -o output/orders.json \
  --input-format csv \
  --types '{"quantity": "int", "unit_price": "float"}'
```

### Programmatic Usage

```python
from myapp.etl import (
    ETLPipeline,
    CSVExtractor,
    JSONLoader,
    Transformer,
    lowercase_keys,
    filter_records,
    compute_field,
)

# Build a pipeline
pipeline = (
    ETLPipeline()
    .extract_from(CSVExtractor("data/orders.csv"))
    .transform_with(
        Transformer()
        .add(lowercase_keys)
        .add(filter_records(lambda r: r["status"] == "completed"))
        .add(compute_field("total", lambda r: r["qty"] * r["price"]))
    )
    .load_to(JSONLoader("output/completed_orders.json"))
)

# Run it
stats = pipeline.run()
print(f"Processed {stats.records_loaded} orders")
```

### Available Transformations

| Transformation | Description |
|----------------|-------------|
| `clean_whitespace` | Strip whitespace from string values |
| `lowercase_keys` | Convert all field names to lowercase |
| `rename_fields(mapping)` | Rename fields using a mapping dict |
| `filter_fields(fields)` | Keep only specified fields |
| `filter_records(condition)` | Drop records not matching condition |
| `validate_required(fields)` | Drop records missing required fields |
| `convert_types(type_map)` | Convert field types (int, float, bool) |
| `compute_field(name, func)` | Add computed field |
| `add_timestamp(name)` | Add processing timestamp |

### Sample Data

The project includes sample data files in the `data/` directory:

- `sample_employees.json` - Employee records with departments and salaries
- `sample_orders.csv` - Order data with products and quantities

## License

MIT License - feel free to use this pipeline for your projects!
