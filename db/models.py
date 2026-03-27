import sqlite3 as sq3
from datetime import datetime as dt

db = "shld_v2.db"

def init():
    with sq3.connect(db) as cx:
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

def ins(fl, msg, sv, ln=0, tid=""):
    with sq3.connect(db) as cx:
        cx.execute(
            "INSERT INTO res (fl, msg, sv, ts, ln, tid) VALUES (?, ?, ?, ?, ?, ?)",
            (fl, msg, sv, dt.now().isoformat(), ln, tid)
        )

def fct():
    with sq3.connect(db) as cx:
        return cx.execute("SELECT * FROM res").fetchall()
