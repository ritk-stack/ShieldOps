import sqlite3 as sq3
from datetime import datetime as dt

DB_PATH = "shld_v2.db"

def init():
    """Create the findings table if it doesn't exist."""
    with sq3.connect(DB_PATH) as cx:
        cx.execute('''
            CREATE TABLE IF NOT EXISTS res (
                id INTEGER PRIMARY KEY,
                fl TEXT,
                msg TEXT,
                sv TEXT,
                ts TEXT,
                ln INTEGER,
                tid TEXT
            )
        ''')

def store_finding(fl, msg, sv, ln=0, tid=""):
    """Insert a single security finding into the database."""
    with sq3.connect(DB_PATH) as cx:
        cx.execute(
            "INSERT INTO res (fl, msg, sv, ts, ln, tid) VALUES (?, ?, ?, ?, ?, ?)",
            (fl, msg, sv, dt.now().isoformat(), ln, tid)
        )

def fetch_all():
    """Retrieve all stored findings."""
    with sq3.connect(DB_PATH) as cx:
        return cx.execute("SELECT * FROM res").fetchall()
