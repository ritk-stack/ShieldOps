import subprocess as sp
import json as js
import os

def run_scan(pth):
    """Run Bandit security scanner on the given path via subprocess."""
    if not os.path.exists(pth):
        return []

    cmd = ["bandit", "-r", pth, "-f", "json"]
    rs = sp.run(cmd, capture_output=True, text=True)

    # Bandit returns 0 for clean, 1 for issues found
    if rs.returncode not in (0, 1):
        print(f"[ERROR] Bandit failed with exit code {rs.returncode}")
        return []

    try:
        dt = js.loads(rs.stdout)
        return dt.get("results", [])
    except js.JSONDecodeError:
        print("[ERROR] Failed to parse Bandit output")
        return []
