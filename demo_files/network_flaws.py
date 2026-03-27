import ssl
import requests
import xmlrpc.client

# B501: Requests with SSL verification disabled
resp = requests.get("https://api.example.com", verify=False)

# B309: Use of HTTPSConnection without certificate verification
import http.client
conn = http.client.HTTPSConnection("example.com")

# B411: Import of xmlrpc (vulnerable to XML attacks)
proxy = xmlrpc.client.ServerProxy("http://example.com/rpc")

# B506: Use of yaml.load without SafeLoader
import yaml
data = yaml.load(open("config.yml"), Loader=yaml.FullLoader)

# B110: try/except/pass (silently swallowing errors)
try:
    resp = requests.get("http://internal-service:8080/health")
except Exception:
    pass

# B104: Binding to all interfaces
import socket
s = socket.socket()
s.bind(("0.0.0.0", 9999))
