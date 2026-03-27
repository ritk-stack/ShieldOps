from scanner.bandit_runner import run_scan
from parser.parse_results import parse_results
from db.models import store_finding

def run_pipeline(pth):
    """kicks off the full scan pipeline on a given path"""
    print(f"[START] scanning: {pth}")

    raw = run_scan(pth)
    print(f"[SCAN DONE] found {len(raw)} raw issues")

    findings = parse_results(raw)
    print(f"[PARSED] {len(findings)} filtered issues")

    for f in findings:
        store_finding(f["fl"], f["msg"], f["sv"], f.get("ln", 0), f.get("tid", ""))

    print(f"[STORED] {len(findings)} issues saved")
    return len(findings)
