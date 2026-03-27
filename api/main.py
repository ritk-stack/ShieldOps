from fastapi import FastAPI
from pydantic import BaseModel
from pipeline.orchestrator import rn
from db.models import init, fct

app = FastAPI()

@app.get("/")
def rt():
    return {"msg": "ShieldOps API"}

class Rq(BaseModel):
    pth: str

@app.on_event("startup")
def st():
    init()

@app.post("/scan")
def dscn(rq: Rq):
    n = rn(rq.pth)
    return {
        "status": "completed",
        "issues_found": n,
        "path": rq.pth
    }

@app.get("/results")
def gr():
    rs = fct()
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
def gr_high():
    rs = fct()
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
def cnt():
    return {"total": len(fct())}

@app.get("/summary")
def sm():
    rs = fct()
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
def hlth():
    return {"status": "ok", "service": "ShieldOps"}
