import os
import sqlite3

# Demo file: mixed vulnerabilities (intentionally vulnerable for testing)

def run_dangerous_commands(user_input):
    # HIGH: OS Command Injection
    os.system("cat /dev/null " + user_input)

    # HIGH: Hardcoded password
    password = "change_me_in_production"

    # MEDIUM: SQL Injection
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 WHERE name = '%s'" % user_input)

run_dangerous_commands("test")
