Checking if your UI ports (4040–4060) on Master node are open from edge node or brownfield nodes

# 1. The Local Check (SSH + Netstat)

Even if the AWS firewall is open, the ports won't respond if Spark or your application isn't actively listening on them.
SSH into your Master node and run:

```bash
# Check if any service is listening on ports 4040 through 4060
netstat -tuln | grep -E '40[4-6][0-9]'
```

* **Look for `LISTEN`:** You want to see entries like `0.0.0.0:4040` or `:::4040` with the status `LISTEN`.
* **Empty Result:** This means your application (like a Spark Driver) isn't running, or it's bound to a different port.

---

# 2. The Connectivity Test (External)

From a machine within the **10.28.0.0** subnet, you can test the path through the security group using `nc` (netcat) or
`telnet`. Replace `MASTER_IP` with the private IP of your EMR Master.

```bash
# Test a specific port like 4040
nc -zv MASTER_IP 4040
```

* **Success:** `Connection to MASTER_IP 4040 port [tcp/*] succeeded!`
* **Failure:** `Connection refused` (Service is down) or `Operation timed out` (Security Group is blocking you or
  something else).
