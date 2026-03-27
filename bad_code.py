import os
import sqlite3

def dangerous_function(user_input):
    # HIGH severity: Command injection
    os.system("ls " + user_input)
    
    # MEDIUM severity: SQL Injection vulnerability
    conn = sqlite3.connect("test.db")
    conn.execute("SELECT * FROM users WHERE name = '" + user_input + "'")
    
    # HIGH severity: Hardcoded password
    secret_db_password = "supersecretpassword123!"

dangerous_function("test")
