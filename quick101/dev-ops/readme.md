# What is  DevOps,CI/CD

DevOps and CI/CD are closely connected as complementary approaches that enhance software development and delivery.

- DevOps is a cultural philosophy and set of practices that emphasize collaboration and integration between software
  development (Dev) and IT operations (Ops) teams. Its goal is to improve software quality, speed, and reliability
  through automation, process improvement, and continuous feedback.

- CI/CD (Continuous Integration and Continuous Delivery/Deployment) is a core set of automated practices within DevOps.
  Continuous Integration means developers frequently merge code changes into a shared repository where automated builds
  and tests run to detect issues early. Continuous Delivery automates preparing tested code for deployment, making
  releases smoother and faster. Continuous Deployment extends this by automatically deploying every successful change to
  production without manual intervention.

Popular tools used to implement CI/CD pipelines include:

- **Jenkins**: Open-source automation server known for its extensive plugin ecosystem and flexibility to support
  building, testing, and deployment automation.
- **GitHub Actions**: GitHub's native CI/CD tool, allowing automation directly within GitHub repositories

### Jenkins pipeline

Jenkins pipeline triggers when code is checked into a Git repository primarily through either polling or webhook
mechanisms. Here's how it works in detail:

- Polling SCM: Jenkins can be configured to poll the Git repository periodically to check for changes. If it detects new
  commits, it triggers the pipeline build. However, this can be inefficient and lead to unnecessary checks.
- Webhook Trigger: A more efficient and common method is using webhooks. When code is pushed to the Git repository (
  e.g., GitHub, GitLab, Bitbucket), the Git server sends a notification to Jenkins using a webhook URL. This instantly
  triggers the Jenkins pipeline job.

To set up both webhook trigger and Poll SCM in Jenkins to automate pipeline runs when code is checked into a Git
repository, follow these steps:

### 1. Set up Webhook Trigger in Git Repository

- Go to your Git repository hosting service (GitHub, GitLab, Bitbucket).
- Navigate to the repository settings and find the section for Webhooks.
- Add a new webhook.
- Set the Payload URL to your Jenkins Git plugin's webhook URL, typically:
  ```
  http://YOUR_JENKINS_URL/jenkins/git/notifyCommit?url=YOUR_GIT_REPO_URL
  ```
- Select the event to trigger on, usually "Push events" or "Push & Merge".
- Save the webhook settings.

### 2. Configure Jenkins Pipeline Job for Poll SCM

- In Jenkins, go to your pipeline job configuration.
- Under "Build Triggers", check the box for "Poll SCM".
- In the schedule field, you can keep this blank if you want Jenkins to rely solely on webhook notifications for
  triggering. If you want Jenkins to poll periodically in addition to webhook triggers, provide a cron expression (e.g.,
  `H/5 * * * *` to poll every 5 minutes).
- Save the job configuration.

### 3. Optional Jenkins Plugin Setup

- Ensure Jenkins has the Git plugin installed.
- For GitHub, install and configure the "GitHub Integration Plugin" or "GitHub Branch Source Plugin" which helps with
  webhook and SCM integrations.
- Make sure Jenkins URL is accessible from the internet or Git server to receive webhook POST requests.

### How It Works Together

- The webhook notifies Jenkins of a new commit immediately.
- On receiving the webhook, Jenkins triggers a Poll SCM action without waiting for the scheduled poll.
- Jenkins checks out the latest code and runs the pipeline.
- If scheduled polling is enabled, Jenkins also polls for changes periodically as a fallback.

This setup ensures quick triggering from webhooks with a backup mechanism from polling to avoid missed triggers. It
improves CI/CD efficiency and responsiveness.

## Summary

Together, CI/CD provides the automation engine that powers DevOps workflows. They automate code integration, testing,
packaging, and deployment pipelines to enable rapid, reliable software delivery with minimal manual steps. This
integration fosters faster feedback loops, higher code quality, and more frequent releases — all central goals of DevOps
culture.

**In summary, DevOps sets the cultural and organizational foundation, while CI/CD implements key automation practices
that realize DevOps objectives of speed, quality, and collaboration in software delivery.**

## DevOps

The DevOps lifecycle generally includes the following phases:

1. Plan — gathering requirements and planning the project.
2. Code — writing source code using version control systems like Git.
3. Build — compiling and building the code into packages.
4. Test — running automated tests.
5. Release — preparing software for release.
6. Deploy — deploying software to environments.
7. Operate — managing the live software.
8. Monitor — monitoring performance and user feedback.

A Python project can illustrate these phases with scripts and integration to tools:

- such as GitHub for source code
- Jenkins or GitHub Actions for building and testing
- Docker for deploying, and monitoring tools to track application health.
  We can automate tasks like these triggering builds, running tests, deploying containers, and collecting logs or
  metrics.

## CI/CD pipeline

A CI/CD pipeline is an automated workflow used in software development to streamline how code is integrated, tested, and
deployed efficiently and reliably.

- **CI (Continuous Integration)** means developers frequently merge small code changes into a shared repository. The
  changes are automatically built and tested to catch errors early.
- **CD (Continuous Delivery or Deployment)** automates releasing code after passing tests. Continuous Delivery prepares
  code for release, usually to a staging environment, with possible manual approval. Continuous Deployment goes further
  by automatically pushing changes to production.

A simple example of a CI/CD pipeline might look like this:

1. Developer commits code to Git repository.
2. Automated system triggers build and runs unit tests on the new code.
3. If tests pass, the system packages the application (e.g., creates a Docker image).
4. The packaged app is deployed to a staging environment for further testing or directly deployed to production if
   continuous deployment is enabled.

The CI/CD pipeline reduces manual work, minimizes bugs by catching problems early via automation, and speeds up software
delivery to users.

This approach is fundamental to DevOps, enabling teams to continuously and safely improve their software with rapid
feedback and automated processes.

## Configure jenkins

In Jenkins, when you configure "Poll SCM" as a build trigger, you specify the Git repository in the same job
configuration where you set up the source code management (SCM) settings for the pipeline or job.

Here’s where to specify the Git repository:

1. **Go to your Jenkins job or pipeline configuration.**
2. **Locate the "Source Code Management" section:**
    - Select "Git" as the SCM.
3. **Enter the Git repository URL:**
    - This is the HTTP(s) or SSH URL of your Git repository (e.g., `https://github.com/user/repo.git`).
4. **Provide credentials if required** for private repositories.
5. **Then, under the "Build Triggers" section, enable "Poll SCM" and specify the schedule** (or leave it blank to rely
   on webhook triggers).

Jenkins uses the Git repository URL under the SCM section to poll for changes when the Poll SCM trigger is active.
Without specifying the Git repo in SCM, polling cannot detect changes.

So, the repo URL is set in the SCM configuration, not in the Poll SCM trigger itself. Poll SCM just tells Jenkins when
to check that configured repository for changes.
