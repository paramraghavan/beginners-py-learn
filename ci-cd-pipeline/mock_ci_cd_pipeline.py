import time
import random


def step(name, success=True, delay=1):
    print(f"\n--- {name} ---")
    time.sleep(delay)

    if success:
        print(f"{name}: SUCCESS")
        return True
    else:
        print(f"{name}: FAILED")
        return False


def developer_push():
    print("Developer writes code...")
    time.sleep(1)
    print("Code pushed to feature branch.")


def run_ci():
    print("\nRunning CI(continuous integration) pipeline...")
    print("\nIn some place CI happen only when PR is raised...")
    checks = [
        "Checkout code",
        "Install dependencies",
        "Run lint checks",
        "Run unit tests",
        "Run fortify scan"
    ]

    for check in checks:
        if not step(check):
            return False

    return True


def pull_request_review():
    print("\nCreating Pull Request to main...")
    time.sleep(1)
    print("Code review in progress...")
    time.sleep(1)
    print("PR approved.")
    return True


def merge_to_main():
    print("\nMerging to main branch...")
    time.sleep(1)
    print("Merge complete.")


def build_artifact():
    return step("Build artifact and push to registry")


def deploy_to_staging():
    print("\nDeploying to staging...")
    if not step("Deploy app to staging"):
        return False
    if not step("Run smoke tests in staging"):
        return False
    return True


def manual_approval():
    print("\nWaiting for manual approval...")
    time.sleep(1)

    approved = True  # change to False to simulate rejection
    if approved:
        print("Manual approval granted.")
        return True
    else:
        print("Manual approval denied.")
        return False


def deploy_to_production():
    print("\nDeploying to production...")
    if not step("Deploy same artifact to production"):
        return False
    if not step("Run production health checks"):
        return False
    return True


def monitor_and_rollback():
    print("\nMonitoring production...")
    time.sleep(1)

    issue_found = random.choice([False, False, True])  # mostly no issue
    if issue_found:
        print("Issue detected in production!")
        print("Rolling back to previous stable version...")
        time.sleep(1)
        print("Rollback complete.")
    else:
        print("System healthy. No rollback needed.")


def main():
    print("=== MOCK CI/CD PIPELINE SIMULATION ===")

    developer_push()

    if not run_ci():
        print("\nPipeline stopped: CI failed.")
        return

    if not pull_request_review():
        print("\nPipeline stopped: PR not approved.")
        return

    merge_to_main()

    if not build_artifact():
        print("\nPipeline stopped: Artifact build failed.")
        return

    if not deploy_to_staging():
        print("\nPipeline stopped: Staging deployment failed.")
        return

    if not manual_approval():
        print("\nPipeline stopped: Approval not granted.")
        return

    if not deploy_to_production():
        print("\nPipeline stopped: Production deployment failed.")
        return

    monitor_and_rollback()

    print("\n=== PIPELINE COMPLETE ===")


if __name__ == "__main__":
    main()