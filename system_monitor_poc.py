import subprocess
import re
import json
from datetime import datetime

# --- Configuration ---
# Use the host machine's tools for the PoC testing
SYSTEM_HOST_CMD = "uname -a && lscpu && echo '--- End System Info ---'"
GPU_CMD = "nvidia-smi"
SERVICE_CMD = "systemctl --user status ezybiz-scraper --no-pager"

def run_command(command):
    """Helper function to execute shell commands and return structured output."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            check=True, 
            timeout=15
        )
        return result.stdout, None
    except subprocess.CalledProcessError as e:
        return e.stderr, f"Command failed with exit code {e.returncode}: {e.stderr}"
    except subprocess.TimeoutExpired:
        return "", "Command timed out after 15 seconds."
    except FileNotFoundError:
        return "", "Required command/tool not found on the system."

def get_system_info():
    """Gathers OS, CPU, and basic hardware info."""
    print("--- Running System Hardware Diagnostics ---")
    output, error = run_command(SYSTEM_HOST_CMD)
    if error:
        print(f"Error gathering system info: {error}")
        return None, error
    return output, None

def get_gpu_info():
    """Parses the output of nvidia-smi for GPU details."""
    print("--- Running GPU Diagnostics ---")
    output, error = run_command(GPU_CMD)
    if error:
        print(f"Error gathering GPU info: {error}")
        return None, error
    return output, None

def get_service_status():
    """Checks the status of the ezybiz-scraper service on the remote machine."""
    # Note: For a true PoC, this should ideally run on the target machine (Mantis),
    # but for local testing, we simulate the structure check.
    print("--- Running Service Status Check ---")
    # Reusing the command from exec for simulation, but acknowledging it should run remotely.
    output, error = run_command(SERVICE_CMD)
    if error:
        print(f"Error gathering service status: {error}")
        return None, error
    return output, None

def generate_report():
    """Gathers all diagnostics and prints a structured report."""
    print("\\n==================================================")
    print("🚀 System Monitor PoC Report Generator 🚀")
    print("==================================================")

    # 1. Get System Info
    sys_info, sys_error = get_system_info()
    if sys_info:
        print("\\n[✅ System Hardware Info]:")
        print(sys_info)
    else:
        print(f"\n[❌ System Hardware Info]: Could not retrieve data. Error: {sys_error}")

    # 2. Get GPU Info
    gpu_info, gpu_error = get_gpu_info()
    if gpu_info:
        print("\n[✅ GPU Details (nvidia-smi Output)]:")
        print(gpu_info)
    else:
        print(f"\n[❌ GPU Details]: Could not retrieve data. Error: {gpu_error}")

    # 3. Get Service Status
    service_status, svc_error = get_service_status()
    if service_status:
        print("\n[✅ Service Status (ezybiz-scraper)]: ")
        print(service_status)
    else:
        print(f"\n[❌ Service Status]: Could not retrieve data. Error: {svc_error}")

if __name__ == "__main__":
    generate_report()