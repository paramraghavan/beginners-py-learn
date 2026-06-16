Yes. Treat this as a **workload-discovery and controlled-cutover project**, not simply a server copy. A process that runs monthly, quarter-end, after a file arrives, or only after another job succeeds will not necessarily appear in today’s `ps` output.

The safest approach is to inventory the server from several independent sources:

1. Current processes, services, ports and containers.
2. Cron, systemd timers, `at`, AutoSys and Control-M.
3. Scheduler history and operating-system logs.
4. Python runtime, configuration and external dependencies.
5. Parallel validation before disabling Brownfield.

I am assuming the AWS edge node is Linux-based, such as an EC2 or EMR edge node.

## 1. Capture a baseline before changing anything

Create a protected discovery directory:

```bash
sudo mkdir -p /var/tmp/brownfield_discovery
sudo chmod 700 /var/tmp/brownfield_discovery

OUT=/var/tmp/brownfield_discovery
HOST=$(hostname -s)
DATE=$(date +%Y%m%d_%H%M%S)
```

Capture basic server information:

```bash
{
    echo "Collection time: $(date --iso-8601=seconds)"
    echo "Hostname: $(hostname -f)"
    echo "Kernel: $(uname -a)"
    echo
    cat /etc/os-release 2>/dev/null
    echo
    uptime
    timedatectl 2>/dev/null
} | sudo tee "$OUT/${HOST}_${DATE}_system.txt"
```

Time zone is important. A cron entry at `02:00` on Brownfield can run at a different actual time if the AWS node uses UTC.

---

## 2. Find everything running now

### Processes

```bash
sudo ps -eo user,pid,ppid,lstart,etime,%cpu,%mem,args \
    --sort=-%cpu > "$OUT/${HOST}_${DATE}_processes.txt"

sudo pstree -ap > "$OUT/${HOST}_${DATE}_process_tree.txt"
```

Search specifically for Python applications and schedulers:

```bash
sudo ps -efww | grep -Ei \
'python|java|shell|bash|cybAgent|autosys|control.?m|ctmag|ctm|airflow|supervisor|celery' \
| grep -v grep
```

### Systemd services

```bash
sudo systemctl list-units \
    --type=service --all --no-pager \
    > "$OUT/${HOST}_${DATE}_services_all.txt"

sudo systemctl list-unit-files \
    --type=service --no-pager \
    > "$OUT/${HOST}_${DATE}_service_files.txt"

sudo systemctl list-units \
    --type=service --state=running --no-pager
```

For every application service you find, capture its full definition:

```bash
sudo systemctl cat my-application.service

sudo systemctl show my-application.service \
    -p User \
    -p Group \
    -p ExecStart \
    -p WorkingDirectory \
    -p EnvironmentFiles \
    -p Restart
```

Do not rely only on `systemctl status`; the application may be started through `/etc/rc.local`, an init script, Supervisor, Docker, or a user login script.

### Older startup mechanisms

```bash
sudo ls -la /etc/init.d/
sudo cat /etc/rc.local 2>/dev/null
sudo find /etc/rc*.d -type l -ls 2>/dev/null
```

### Containers and process managers

```bash
command -v docker >/dev/null && sudo docker ps --no-trunc
command -v podman >/dev/null && sudo podman ps --no-trunc
command -v supervisorctl >/dev/null && sudo supervisorctl status
command -v pm2 >/dev/null && pm2 list
```

### Listening ports and active connections

```bash
sudo ss -lntup > "$OUT/${HOST}_${DATE}_listening_ports.txt"
sudo ss -tpn state established > "$OUT/${HOST}_${DATE}_connections.txt"
sudo lsof -nP -i 2>/dev/null > "$OUT/${HOST}_${DATE}_network_lsof.txt"
```

This can reveal inbound APIs, file-transfer listeners, database connections and calls to downstream systems.

---

## 3. Find cron, systemd timers and other local schedules

### All users’ crontabs

Do not check only your own account.

```bash
sudo bash -c '
for user in $(cut -d: -f1 /etc/passwd); do
    cron=$(crontab -u "$user" -l 2>/dev/null) || continue
    if [ -n "$cron" ]; then
        echo
        echo "===== USER: $user ====="
        echo "$cron"
    fi
done
' | tee "$OUT/${HOST}_${DATE}_user_crontabs.txt"
```

### System cron files

```bash
sudo cat /etc/crontab 2>/dev/null

sudo find \
    /etc/cron.d \
    /etc/cron.hourly \
    /etc/cron.daily \
    /etc/cron.weekly \
    /etc/cron.monthly \
    -maxdepth 2 -type f -print \
    -exec sed -n '1,250p' {} \; 2>/dev/null \
    | tee "$OUT/${HOST}_${DATE}_system_cron.txt"
```

Also inspect the cron spool directly:

```bash
sudo find /var/spool/cron /var/spool/cron/crontabs \
    -type f -ls 2>/dev/null
```

### Anacron and one-time `at` jobs

```bash
sudo cat /etc/anacrontab 2>/dev/null
sudo atq 2>/dev/null
```

### Systemd timers

```bash
sudo systemctl list-timers --all --no-pager \
    | tee "$OUT/${HOST}_${DATE}_systemd_timers.txt"
```

`systemctl list-timers --all` shows each timer’s last and next activation. For a timer you find:

```bash
sudo systemctl cat example.timer
sudo systemctl cat example.service

sudo journalctl \
    -u example.timer \
    -u example.service \
    --since "90 days ago" \
    --no-pager
```

Systemd officially provides `list-timers` for inspecting timer units. ([Freedesktop.org][1])

---

## 4. Detect AutoSys

Search for running agents, installed commands and installation directories:

```bash
sudo ps -efww | grep -Ei \
'cybAgent|autosys|wa[_-]?agent' | grep -v grep

command -v cybAgent
command -v autosyslog
command -v autorep
command -v sendevent

sudo find /opt /app /usr/local /home \
    -type f \
    \( -name 'cybAgent' \
       -o -name 'cybAgent.bin' \
       -o -name 'autosyslog' \
       -o -name 'autorep' \) \
    2>/dev/null
```

If `cybAgent` is found, use the executable from its installation directory:

```bash
/path/to/cybAgent -vv
```

Broadcom documents `cybAgent` as the agent-control command, and `cybAgent -vv` can display installed plug-ins, integrations and build information. AutoSys agent logs are normally stored in a `log` directory under the agent installation directory. ([TechDocs][2])

Search the likely agent logs and spool files:

```bash
sudo find /opt /app /usr/local \
    -type f \
    \( -path '*/log/*' -o -path '*/spool/*' \) \
    -mtime -100 \
    2>/dev/null
```

The most important AutoSys check must be performed centrally:

> Ask the AutoSys administrator to search all job definitions whose machine, agent name, hostname or alias points to Brownfield.

Export:

* Job name and box name.
* Command or script.
* Machine/agent field.
* Run-as user.
* Calendar and start conditions.
* File watchers.
* Dependencies and predecessor jobs.
* Environment profiles.
* Last 90 days of executions.
* Standard output, error and agent log locations.

AutoSys `autorep` reports defined jobs and machines, while WCC can display previous runs and prior standard-output, error and agent logs. ([TechDocs][3])

Do not assume “no AutoSys process on this server” means “no AutoSys jobs.” Brownfield may be configured as a remote execution host or referenced through an alias.

---

## 5. Detect Control-M

Search for the agent and utilities:

```bash
sudo ps -efww | grep -Ei \
'control.?m|ctmag|ctm|p_ctm' | grep -v grep

command -v start-ag
command -v shut-ag
command -v ag_diag_comm

sudo find /opt /app /usr/local /home \
    -type f \
    \( -name 'start-ag' \
       -o -name 'shut-ag' \
       -o -name 'ag_diag_comm' \) \
    2>/dev/null
```

Do **not** run `start-ag` or `shut-ag` during discovery. Their presence is enough to identify a possible agent. BMC documents these as the UNIX utilities for starting and stopping Control-M/Agent, and `ag_diag_comm` produces an Agent communication diagnostic report. ([BMC Documents][4])

Locate Control-M logs:

```bash
sudo find /opt /app /usr/local /home \
    -type d \
    \( -name proclog -o -name dailylog \) \
    -print 2>/dev/null

sudo find /opt /app /usr/local /home \
    -type f \
    \( -path '*/proclog/*' \
       -o -path '*/dailylog/*' \
       -o -name 'daily_ctmag_*.log' \) \
    -mtime -100 \
    -ls 2>/dev/null
```

Control-M Agent process logs are maintained in `proclog`, and daily job information can be written to files named like `daily_ctmag_YYYYMMDD.log`. Retention is configurable and can be quite short: BMC documents defaults of one day for Agent logs and seven days for usage daily logs in some configurations. Therefore, the central Control-M server or Enterprise Manager should be treated as the authoritative history source. ([BMC Documents][5])

Ask the Control-M administrator to filter definitions and history by:

* Host or Agent name.
* Host group.
* Run-as user.
* Brownfield hostname, short name, FQDN, IP and aliases.
* Script path.
* Application and subapplication.
* File watcher paths.
* Last 90 days of orders and executions.

---

## 6. Determine what ran during the last 90 days

There is one major limitation:

**Linux does not automatically preserve a complete, searchable history of every process for 90 days.** You can reconstruct history only from logs, scheduler history, process accounting, audit logs or monitoring systems that were already enabled. Process accounting tools such as `lastcomm` read records collected by `acct`/`psacct`; installing them now will help going forward but will not recreate past activity. ([man7.org][6])

### Cron history from systemd journal

```bash
sudo journalctl \
    -u crond.service \
    -u cron.service \
    --since "90 days ago" \
    --output=short-iso \
    --no-pager \
    | tee "$OUT/${HOST}_${DATE}_cron_90days.txt"
```

Get a rough execution count by command:

```bash
sudo journalctl \
    -u crond.service \
    -u cron.service \
    --since "90 days ago" \
    --no-pager \
| grep -E 'CMD|COMMAND' \
| sed -E 's/^.*CMD[[:space:]]*\((.*)\).*$/\1/' \
| sort \
| uniq -c \
| sort -nr
```

### Traditional cron log files

Red Hat/Amazon Linux commonly uses `/var/log/cron`; Ubuntu/Debian frequently records cron activity in syslog.

```bash
sudo zgrep -hEi 'CRON|CROND' \
    /var/log/cron* \
    /var/log/syslog* \
    /var/log/messages* \
    2>/dev/null \
    | tee "$OUT/${HOST}_${DATE}_cron_files.txt"
```

### Check journal retention

```bash
sudo journalctl --list-boots
sudo journalctl --disk-usage
sudo journalctl --since "90 days ago" -n 20
```

Journal retention and persistence depend on the server’s journald configuration and disk limits, so 90 days might not be available. ([Freedesktop.org][7])

### Process accounting

```bash
sudo systemctl status psacct 2>/dev/null
sudo systemctl status acct 2>/dev/null

command -v lastcomm >/dev/null && sudo lastcomm | head -100
```

If enabled, useful searches include:

```bash
sudo lastcomm python
sudo lastcomm bash
sudo lastcomm your_service_user
```

### Audit history

Check whether audit rules existed:

```bash
sudo systemctl status auditd 2>/dev/null
sudo auditctl -l 2>/dev/null
```

If execution auditing was previously enabled:

```bash
START=$(date --date='90 days ago' '+%m/%d/%Y')

sudo ausearch \
    -m EXECVE \
    -ts "$START" \
    -i > "$OUT/${HOST}_${DATE}_audit_exec_90days.txt"
```

An empty result does not prove that nothing ran; it may mean execution auditing was not configured.

### Shell history

```bash
sudo find /root /home \
    -maxdepth 2 \
    -type f \
    \( -name '.bash_history' \
       -o -name '.zsh_history' \
       -o -name '.python_history' \) \
    -ls 2>/dev/null
```

Shell history is only supporting evidence. It can be incomplete, manually cleared, missing timestamps, or bypassed by schedulers and services.

### Application logs modified during the last 90 days

```bash
sudo find /var/log /opt /app /srv \
    -type f -mtime -90 \
    -printf '%TY-%Tm-%Td %TH:%TM %s %p\n' \
    2>/dev/null \
    | sort > "$OUT/${HOST}_${DATE}_recent_logs.txt"
```

Also search logs for Python script names and directories discovered earlier:

```bash
sudo grep -RIl \
    '/path/to/application\|script_name.py' \
    /var/log /opt /app 2>/dev/null
```

---

## 7. Inventory the Python environment

For each Python application record:

* Python executable and version.
* Virtual environment.
* Requirements or lock file.
* Service user and group.
* Working directory.
* Environment files.
* Input and output locations.
* Network/database dependencies.
* Certificates.
* Native Linux packages.
* Time zone and locale.

Commands:

```bash
which python python3 2>/dev/null
python3 --version 2>/dev/null

sudo find /opt /app /srv /home \
    -maxdepth 5 \
    -type f \
    \( -name '*.py' \
       -o -name 'requirements*.txt' \
       -o -name 'pyproject.toml' \
       -o -name 'Pipfile' \
       -o -name 'poetry.lock' \
       -o -name 'uv.lock' \) \
    2>/dev/null
```

Find virtual environments:

```bash
sudo find /opt /app /srv /home \
    -type f -path '*/bin/python*' \
    -ls 2>/dev/null
```

For each virtual environment:

```bash
/path/to/venv/bin/python --version
/path/to/venv/bin/python -m pip freeze
/path/to/venv/bin/python -c "
import sys, platform
print(sys.executable)
print(sys.version)
print(platform.platform())
"
```

Check shared-library dependencies for packages with native code:

```bash
ldd /path/to/venv/bin/python
```

Do not blindly copy the Brownfield virtual environment to AWS. Recreate it from a locked dependency file on the AWS node because compiled packages may depend on the original operating system and libraries.

---

## 8. Capture filesystem and external dependencies

```bash
findmnt > "$OUT/${HOST}_${DATE}_mounts.txt"
df -hT > "$OUT/${HOST}_${DATE}_disk.txt"
sudo cat /etc/fstab > "$OUT/${HOST}_${DATE}_fstab.txt"
```

Look for NFS, EFS, shared directories, inbound files and symbolic links:

```bash
sudo find /opt /app /srv \
    -type l -ls 2>/dev/null

sudo lsof +D /important/application/path 2>/dev/null
```

Capture package inventory:

```bash
command -v rpm >/dev/null && \
    rpm -qa | sort > "$OUT/${HOST}_${DATE}_rpm_packages.txt"

command -v dpkg-query >/dev/null && \
    dpkg-query -W > "$OUT/${HOST}_${DATE}_deb_packages.txt"
```

Review environment variables carefully:

```bash
sudo systemctl show my-application.service \
    -p EnvironmentFiles \
    -p Environment
```

Avoid writing passwords, API keys, database credentials or tokens into the discovery report. On AWS, move them to IAM roles, Secrets Manager or Systems Manager Parameter Store rather than copying plaintext configuration files.

---

## 9. Build a migration matrix

Create one row for every workload:

| Field                 | Example                                 |
| --------------------- | --------------------------------------- |
| Component             | Customer reconciliation                 |
| Type                  | AutoSys / Control-M / cron / service    |
| Schedule              | Monday–Friday at 02:00 ET               |
| Command               | `/opt/app/venv/bin/python reconcile.py` |
| Run-as user           | `appsvc`                                |
| Working directory     | `/opt/app/reconcile`                    |
| Environment file      | `/etc/app/reconcile.env`                |
| Inputs                | S3, NFS, database table                 |
| Outputs               | Database, report file, API              |
| Upstream dependency   | File watcher / previous job             |
| Downstream dependency | Reporting job                           |
| Logs                  | `/var/log/app/reconcile.log`            |
| SLA                   | Complete by 05:00                       |
| AWS target            | Edge node path/service                  |
| Validation            | Row counts and checksum                 |
| Rollback              | Re-enable Brownfield definition         |

Do not approve cutover while any discovered entry lacks an owner, purpose, schedule, dependencies, target and validation method.

---

## 10. Migrate without duplicate processing

A safe sequence is:

### Discovery

Complete the inventory and obtain central AutoSys/Control-M exports. Include monthly and event-driven jobs, not only daily jobs.

### Build

Recreate:

* Users and groups.
* Directories and permissions.
* Python environment.
* Systemd service definitions.
* Network rules.
* Mounts and shared storage.
* Certificates.
* IAM permissions.
* Secrets.
* Logging and monitoring.

### Dry run

Run each job manually on AWS with:

* Production writes disabled, or
* A test database/schema, or
* A separate S3/output prefix.

Capture:

```bash
date
hostname
whoami
pwd
env | sort       # redact secrets
python --version
command arguments
exit code
start/end time
input count
output count
```

### Parallel validation

For suitable jobs, run Brownfield and AWS against the same input but direct AWS output to a comparison location.

Compare:

* Record counts.
* File sizes.
* Checksums.
* Database totals.
* Rejected records.
* Runtime.
* Exit status.
* Downstream notifications.
* File ownership and permissions.

### Cutover

1. Freeze code and scheduler-definition changes.
2. Confirm there are no active jobs on Brownfield.
3. Disable the Brownfield schedule.
4. Enable the AWS schedule.
5. Watch the first executions live.
6. Validate downstream consumers.
7. Keep Brownfield available but disabled during the rollback period.

Use an application-level execution lock or run ledger so the same business date cannot be processed twice. A lock should be based on a durable shared system such as a database row, DynamoDB record or S3 marker—not a local file on one server.

### Rollback

Document in advance:

* How to disable the AWS job.
* How to determine whether AWS partially committed results.
* How to clean up or reverse partial output.
* How to re-enable Brownfield.
* Which business date should be rerun.
* Who authorizes rollback.

---

## Critical warning about the 90-day question

The best evidence order is:

1. **Central AutoSys or Control-M execution history.**
2. Application and scheduler logs.
3. Cron/systemd journal logs.
4. Audit or process-accounting records.
5. Monitoring data.
6. Shell history.

When Brownfield has only seven or thirty days of local logs, the central scheduler database, enterprise log platform, Splunk, CloudWatch, ELK or backup archives may still contain the complete 90-day evidence. Do not retire the server until central scheduling teams confirm that no definitions, aliases, host groups, file watchers or remote jobs still reference it.

[1]: https://www.freedesktop.org/software/systemd/man/systemctl.html?utm_source=chatgpt.com "systemctl"
[2]: https://techdocs.broadcom.com/us/en/ca-mainframe-software/automation/ca-workload-automation-esp-edition/12-0/reference/commands/cybagent-command-control-agents.html?utm_source=chatgpt.com "cybAgent Command: Control Agents - Broadcom TechDocs"
[3]: https://techdocs.broadcom.com/us/en/ca-enterprise-software/intelligent-automation/autosys-workload-automation/12-1/reference/ae-commands/monitor-and-report-on-workload/autorep-command-report-job-machine-and-variable-information.html?utm_source=chatgpt.com "autorep Command -- Report Job, Machine, and Variable ..."
[4]: https://documents.bmc.com/supportu/9.0.21/en-US/Documentation/Agent_Troubleshooting_Utilities.htm?utm_source=chatgpt.com "Agent Troubleshooting Utilities"
[5]: https://documents.bmc.com/supportu/9.0.22/en-US/Documentation/Configuring_Agent_System_Parameters.htm?utm_source=chatgpt.com "Configuring Agent System Parameters"
[6]: https://man7.org/linux/man-pages/man5/acct.5.html?utm_source=chatgpt.com "acct(5) - Linux manual page"
[7]: https://www.freedesktop.org/software/systemd/man/journald.conf.html?utm_source=chatgpt.com "journald.conf"
