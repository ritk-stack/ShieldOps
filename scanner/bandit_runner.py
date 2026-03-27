import subprocess as sp
import json as js
import os

def scn(pth):
    if not os.path.exists(pth):
        return []

    cmd = ["bandit", "-r", pth, "-f", "json"]
    rs = sp.run(cmd, capture_output=True, text=True)
    
    # Bandit returns 0 for no issues, 1 for vulnerabilities found
    if rs.returncode not in (0, 1):
        return []

    try:
        dt = js.loads(rs.stdout)
        return dt.get("results", [])
    except js.JSONDecodeError:
        return []
