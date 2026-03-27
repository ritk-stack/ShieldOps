# ShieldOps

A security pipeline orchestrator that scans Python codebases for vulnerabilities, parses the findings into structured data, and serves them through a REST API.

Built this as a proof-of-concept for automating SAST (Static Application Security Testing) in a DevSecOps workflow.

## How it works

```
POST /scan  →  Bandit subprocess  →  parse raw JSON  →  store in SQLite  →  query via API
```

The idea is simple — you point it at a folder of Python code, it runs [Bandit](https://github.com/PyCQA/bandit) under the hood, filters out the noise, and gives you back clean, structured security findings you can actually act on.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

## Usage

Trigger a scan:
```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"pth": "demo_files"}'
```

Check what it found:
```bash
curl http://localhost:8000/results
curl http://localhost:8000/results/high   # only critical stuff
curl http://localhost:8000/summary        # aggregated risk view
```

Or just open `http://localhost:8000/docs` — FastAPI gives you a full interactive UI for free.

## Endpoints

| Method | Path | What it does |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/scan` | Run security scan on a path |
| GET | `/results` | All findings with file, line, severity, test_id |
| GET | `/results/high` | Filtered to HIGH severity only |
| GET | `/summary` | Severity breakdown + risk level |
| GET | `/count` | Total issue count |

## Project layout

```
├── api/main.py                # FastAPI routes
├── pipeline/orchestrator.py   # scan → parse → store workflow
├── scanner/bandit_runner.py   # subprocess wrapper for Bandit
├── parser/parse_results.py    # normalizes raw output
├── db/models.py               # SQLite operations
└── demo_files/                # intentionally vulnerable test files
```

## What Bandit catches

Command injection (`os.system`, `subprocess(shell=True)`), SQL injection, hardcoded secrets, weak crypto (`md5`, `sha1`), insecure deserialization (`pickle.load`), disabled SSL verification, and more. Full list in the [Bandit docs](https://bandit.readthedocs.io/en/latest/plugins/index.html).

## Design notes

- **Scanner-agnostic** — the orchestrator just calls a function and expects a list back. Swapping Bandit for Semgrep or Trivy is a matter of writing a new runner.
- **SQLite** — zero config, works out of the box. Good enough for local/dev use.
- **Synchronous scanning** — the scan blocks the response so you get results immediately. Could be moved to background tasks for production.

## What I'd add next

- More scanners (Semgrep for multi-language support)
- Background task queue (Celery) for non-blocking scans  
- Slack/Discord webhook alerts on HIGH findings
- CLI mode for CI/CD integration
- Docker packaging

## Tech

Python, FastAPI, Bandit, SQLite, Uvicorn
