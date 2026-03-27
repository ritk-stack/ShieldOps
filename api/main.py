from fastapi import FastAPI
from pydantic import BaseModel
from pipeline.orchestrator import run_pipeline
from db.models import init, fetch_all

app = FastAPI(title="ShieldOps", description="Security Pipeline Orchestrator API")

@app.get("/")
def root():
    return {"msg": "ShieldOps API"}

class ScanRequest(BaseModel):
    pth: str

@app.on_event("startup")
def startup():
    """Initialize database on server start."""
    init()

@app.post("/scan")
def trigger_scan(req: ScanRequest):
    """Trigger a security scan on the given path."""
    n = run_pipeline(req.pth)
    return {
        "status": "completed",
        "issues_found": n,
        "path": req.pth
    }

@app.get("/results")
def get_results():
    """Return all stored findings with full detail."""
    rs = fetch_all()
    return [
        {
            "id": r[0],
            "file": r[1],
            "issue": r[2],
            "severity": r[3],
            "timestamp": r[4],
            "line": r[5],
            "test_id": r[6]
        }
        for r in rs
    ]

@app.get("/results/high")
def get_high_severity():
    """Return only HIGH severity findings."""
    rs = fetch_all()
    return [
        {
            "id": r[0],
            "file": r[1],
            "issue": r[2],
            "severity": r[3],
            "timestamp": r[4],
            "line": r[5],
            "test_id": r[6]
        }
        for r in rs if r[3] == "HIGH"
    ]

@app.get("/count")
def get_count():
    """Return total number of findings."""
    return {"total": len(fetch_all())}

@app.get("/summary")
def get_summary():
    """Return aggregated risk dashboard."""
    rs = fetch_all()
    ct = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    fls = set()
    for r in rs:
        sv = r[3]
        if sv in ct:
            ct[sv] += 1
        fls.add(r[1])
    return {
        "severity_counts": ct,
        "total_issues": len(rs),
        "files_affected": len(fls),
        "risk_level": "CRITICAL" if ct["HIGH"] >= 3 else "HIGH" if ct["HIGH"] >= 1 else "MEDIUM" if ct["MEDIUM"] >= 1 else "LOW"
    }

@app.get("/health")
def health():
    """Service health check."""
    return {"status": "ok", "service": "ShieldOps"}
