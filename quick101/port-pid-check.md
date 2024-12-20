# How find the process ID (PID) I am using port 7000:

On Linux/Mac:

```bash
lsof -i :7000
```

or

```bash
netstat -vanp tcp | grep 7000
```

On Windows:

```cmd
netstat -ano | findstr :7000
```

or

```powershell
Get-NetTCPConnection -LocalPort 7000
```
