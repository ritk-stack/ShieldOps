import os
import subprocess
import sqlite3

# B102: exec() used — arbitrary code execution
user_code = "print('hacked')"
exec(user_code)

# B307: eval() used — arbitrary code execution
val = eval("2 + 2")

# B605: Starting process with shell=True
subprocess.call("ls -la /tmp", shell=True)

# B602: subprocess with shell=True from variable
cmd = "cat /etc/shadow"
subprocess.Popen(cmd, shell=True)

# B605: os.system command injection
os.system("rm -rf " + "/tmp/data")

# B608: SQL injection via string formatting
db = sqlite3.connect(":memory:")
name = "admin"
db.execute("SELECT * FROM users WHERE name = '%s'" % name)

# B609: Wildcard injection in os.system
os.system("tar cf backup.tar *")
