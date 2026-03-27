import pickle
import marshal
import shelve

# B301: Pickle deserialization (arbitrary code execution)
with open("data.pkl", "rb") as f:
    obj = pickle.load(f)

# B302: Marshal deserialization
with open("data.marshal", "rb") as f:
    obj = marshal.load(f)

# B403: Import of pickle module flagged
# (already imported above)

# B502: SSL with no version specified
import ssl
ctx = ssl._create_unverified_context()

# B101: Use of assert in production code
def check_admin(user):
    assert user.is_admin, "Not admin"
    return True
