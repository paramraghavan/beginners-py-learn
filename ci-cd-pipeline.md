# Simple CI/CD Pipeline
This document describes a **simple** continuous integration and continuous delivery (CI/CD) workflow for a typical
application.


```text
           +-------------------+
           |   Developer       |
           |   writes code     |
           +---------+---------+
                     |
                     v
            +--------+--------+
            |   Push to Git   |
            |  (feature/*)    |
            +--------+--------+
                     |
                     v
        +------------+-------------+
        |     CI: Build & Test     |
        |  - Checkout              |
        |  - Lint / Static checks  |
        |  - Unit tests            |
        +------------+-------------+
                     |
                     v
            +--------+--------+
            |  PR to `main`   |
            |  CI re-runs     |
            +--------+--------+
                     |
          PR passes checks & review
                     |
                     v
            +--------+--------+
            |  Merge to main  |
            +--------+--------+
                     |
                     v
        +------------+-------------+
        |  Build Artifact & Push   |
        |  to Artifact Registry    |
        +------------+-------------+
                     |
                     v
        +------------+-------------+
        |   CD: Deploy to Staging  |
        |  - Apply IaC             |
        |  - Smoke tests           |
        +------------+-------------+
                     |
             Manual approval
                     |
                     v
        +------------+-------------+
        |  CD: Deploy to Prod      |
        |  - Reuse same artifact   |
        |  - Smoke tests           |
        |  - Monitor & rollback    |
        +--------------------------+
```



## Goals

- Automatically build and test every commit.
- Ensure main branch is always deployable.
- Automate deployment to staging and production with approvals.

---

## High-Level Flow

1. Developer pushes code to feature branch.
2. CI runs automated checks (lint, unit tests, basic security scans).
3. On pull request to `main`, CI runs the full test suite and quality gates.
4. On merge to `main`, artifacts are built and stored.
5. CD deploys artifacts to staging automatically.
6. After approval, CD deploys the same artifact to production.

---

## Branching Strategy

- `main`: Always releasable, protected; only PR merges allowed.
- `develop` (optional): Integration branch for teams that need it.
- `feature/*`: Short-lived branches for new work and bug fixes.
- `hotfix/*`: Fixes for production issues, merged back to `main` (and `develop` if used).

---

## CI Pipeline Stages

Triggered on:

- Push to any branch.
- Pull request targeting `main`.

Stages:

1. **Checkout**
    - Pull code from the repository.
2. **Install**
    - Install dependencies (for example, `pip install -r requirements.txt` or `npm install`).
3. **Static Checks**
    - Linting (flake8, ESLint, etc.).
    - Formatting checks (black, prettier).
4. **Unit Tests**
    - Run unit tests with coverage thresholds.
5. **Security / Quality (Optional)**
    - SAST tools (Bandit, Semgrep, etc.).
    - Dependency vulnerability scan.
6. **Build Artifact**
    - Build application artifact (Docker image, wheel, JAR, etc.).
    - Tag artifact with version and commit SHA.

Outputs:

- Test reports stored in CI system.
- Build artifact pushed to artifact registry (e.g., Docker registry, artifact repository).

---

## CD Pipeline Stages

Triggered on:

- Successful build from `main` branch.

### 1. Deploy to Staging

- Pull versioned artifact from the registry.
- Apply infrastructure-as-code templates (Terraform, CloudFormation, Helm, etc.).
- Deploy to staging environment.
- Run smoke tests and basic health checks.

Approval:

- If smoke tests pass, staging deployment is marked successful.

### 2. Manual Approval

- A human reviewer validates:
    - Basic app functionality in staging.
    - Logs and metrics show no obvious issues.
- Approver clicks “Approve” in the CD tool to promote to production.

### 3. Deploy to Production

- Reuse the same artifact used in staging (no rebuild).
- Deploy using blue/green, canary, or rolling strategy (depending on risk tolerance).
- Run automated smoke tests in production after deployment.
- Monitor metrics and error rates closely.

Rollback:

- If issues are detected, roll back to the previous stable version via:
    - Previous artifact tag in the registry.
    - Previous infrastructure configuration.

---

## Environments

- **Local**: Developers run tests and services locally using Docker Compose or a local stack.
- **Staging**: Mirrors production as closely as possible; used for full integration testing.
- **Production**: Customer-facing environment with strict access and change control.

---

## Triggers and Rules

- CI:
    - Runs on every push to any branch.
    - Required status checks for PRs into `main`.
- CD:
    - Auto-deploy to staging on successful `main` build.
    - Manual approval gate for production.
    - Only tagged releases (for example, `vX.Y.Z`) allowed to go to production, if desired.

---

## Example Tooling

You can implement this pattern with many stacks, such as:

- Git hosting: GitHub, GitLab, Bitbucket.
- CI: GitHub Actions, GitLab CI, Jenkins, CircleCI.
- CD: Argo CD, Spinnaker, GitHub Actions, GitLab Environments.
- Artifacts: Docker Hub, ECR, GCR, Nexus, Artifactory.
- IaC: Terraform, CloudFormation, Helm, Pulumi.

---

## Best Practices

- Keep pipelines fast (under ~10 minutes when possible).
- Make tests deterministic and reliable.
- Fail fast on linting and unit tests to save resources.
- Version everything: code, configs, artifacts, and IaC.
- Keep production deployments predictable and repeatable (no manual changes on servers).
