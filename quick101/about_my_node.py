import os
import socket
import platform
import sys
import json


def print_node_characteristics():
    """Prints a comprehensive diagnostic of the current execution node."""

    # 1. Networking Info
    hostname = socket.gethostname()
    try:
        # Attempts to get the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
    except Exception:
        ip_address = "Could not determine IP"

    # 2. System/OS Info
    system_info = {
        "Hostname": hostname,
        "IP Address": ip_address,
        "OS": platform.system(),
        "OS Release": platform.release(),
        "Architecture": platform.machine(),
        "Python Version": sys.version.split()[0],
    }

    # 3. Path/Process Info
    process_info = {
        "Current Directory": os.getcwd(),
        "Script File": __file__ if '__file__' in globals() else "REPL/Interactive",
        "Process ID": os.getpid(),
        "Parent PID": os.getppid(),
        "User": os.getlogin() if hasattr(os, 'getlogin') else "Unknown",
    }

    print("=" * 60)
    print("NODE CHARACTERISTICS")
    print("=" * 60)

    print("\n--- System & Network ---")
    for k, v in system_info.items():
        print(f"{k:18}: {v}")

    print("\n--- Process Context ---")
    for k, v in process_info.items():
        print(f"{k:18}: {v}")

    print("\n--- Environment Variables (First 10) ---")
    # We only print the first 10 to avoid a wall of text
    env_vars = list(os.environ.items())
    for k, v in env_vars[:10]:
        print(f"{k:18}: {v}")
    if len(env_vars) > 10:
        print(f"... and {len(env_vars) - 10} more.")

    print("=" * 60)


# Run the diagnostic
if __name__ == "__main__":
    print_node_characteristics()