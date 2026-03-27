import hashlib
import tempfile
import random

# B303: Use of insecure MD5 hash function
password = "mysecretpass"
hashed = hashlib.md5(password.encode()).hexdigest()

# B303: Use of insecure SHA1 hash function
token = hashlib.sha1(b"session_data").hexdigest()

# B306: Use of mktemp (insecure temp file creation)
tmp = tempfile.mktemp()

# B311: Use of random for cryptographic purposes (pseudo-random, not secure)
secret_token = random.randint(100000, 999999)
api_nonce = random.random()
