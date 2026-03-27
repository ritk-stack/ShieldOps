# ShieldOps

A lightweight security pipeline orchestrator that automates vulnerability scanning, normalizes findings into structured signals, and serves them through a REST API.

This project focuses on **orchestration and automation of security tools** rather than building scanners from scratch.

## Why ShieldOps?

Modern engineering teams need automated security pipelines to detect and prioritize vulnerabilities early in development — not after deployment.

ShieldOps simulates a security operations system that:
- Automates vulnerability scanning via pluggable tools
- Aggregates security signals by severity
- Enables API-driven security workflows
- Reduces manual triage by filtering noise

## Key Concepts

- **Security Signal Aggregation** — raw scanner output → structured, prioritized findings
- **Automated Vulnerability Scanning (SAST)** — static analysis on every scan trigger
- **Pipeline Orchestration** — scan → parse → store as a single coordinated workflow
- **Modular Security Tool Integration** — swap Bandit for Semgrep/Trivy without touching the pipeline

## How it works

```
POST /scan  →  Bandit subprocess  →  parse raw JSON  →  store in SQLite  →  query via API
```

You point it at a folder of Python code, it runs [Bandit](https://github.com/PyCQA/bandit) under the hood, filters out the noise, and gives you back clean findings you can act on.

## Example Output

**Trigger a scan:**
```bash
curl -X POST http://localhost:8000/scan -H "Content-Type: application/json" -d '{"pth": "demo_files"}'
```
```json
{
  "status": "completed",
  "issues_found": 15,
  "path": "demo_files"
}
```

**Risk summary:**
```bash
curl http://localhost:8000/summary
```
```json
{
  "severity_counts": { "HIGH": 6, "MEDIUM": 5, "LOW": 4 },
  "total_issues": 15,
  "files_affected": 5,
  "risk_level": "CRITICAL"
}
```

**Detailed findings:**
```bash
curl http://localhost:8000/results
```
```json
[
  {
    "id": 1,
    "file": "demo_files/injection_flaws.py",
    "issue": "subprocess call with shell=True identified",
    "severity": "HIGH",
    "timestamp": "2026-03-27T22:30:01",
    "line": 13,
    "test_id": "B602"
  }
]
```

**Pipeline logs (server terminal):**
```
[START] scanning: demo_files
[SCAN DONE] found 22 raw issues
[PARSED] 15 filtered issues
[STORED] 15 issues saved
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

## Endpoints

| Method | Path | What it does |
|--------|------|-------------|
| GET | `/health` | Service health check |
| POST | `/scan` | Run security scan on a target path |
| GET | `/results` | All findings — file, line, severity, test_id, timestamp |
| GET | `/results/high` | Filtered to HIGH severity only |
| GET | `/summary` | Severity breakdown, files affected, risk level |
| GET | `/count` | Total issue count |

## Project layout

```
├── api/main.py                # FastAPI routes
├── pipeline/orchestrator.py   # scan → parse → store workflow
├── scanner/bandit_runner.py   # subprocess wrapper for Bandit
├── parser/parse_results.py    # normalizes raw scanner output
├── db/models.py               # SQLite schema and operations
└── demo_files/                # intentionally vulnerable test files
```

## Demo Files

The project includes intentionally vulnerable Python files to demonstrate detection capabilities across different vulnerability categories:

| File | Category |
|------|----------|
| `injection_flaws.py` | Command injection, SQL injection, exec/eval |
| `crypto_flaws.py` | Weak hashing (md5/sha1), insecure randomness |
| `hardcoded_secrets.py` | Hardcoded passwords and API keys |
| `network_flaws.py` | Disabled SSL, binding 0.0.0.0, unsafe YAML loading |
| `dangerous_imports.py` | Pickle deserialization, marshal, assert misuse |

## Design notes

- **Scanner-agnostic** — the orchestrator just calls a function and expects a list back. Swapping Bandit for Semgrep or Trivy is a matter of writing a new runner module.
- **SQLite** — zero config, file-based. Good enough for local and dev use.
- **Synchronous scanning** — scan blocks the response so you get results immediately. Could be moved to background tasks for production use.
- **Risk scoring** — the `/summary` endpoint calculates an overall risk level (CRITICAL/HIGH/MEDIUM/LOW) based on severity distribution, not just raw counts.

## What I'd add next

- More scanners (Semgrep for multi-language, Trivy for container scanning)
- Background task queue (Celery) for non-blocking scans
- Slack/Discord alerts on HIGH findings
- CLI mode for CI/CD integration
- Docker packaging

## Tech

Python · FastAPI · Bandit · SQLite · Uvicorn
