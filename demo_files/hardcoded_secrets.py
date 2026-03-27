# Demo file: hardcoded credentials (intentionally vulnerable for testing)
# These are FAKE values used to trigger Bandit security warnings

# B105: Hardcoded password string
DB_PASSWORD = "change_me_in_production"

# B105: API key pattern
API_KEY = "FAKE-KEY-FOR-DEMO-ONLY-000000"

# B105: Connection string with embedded creds
DB_URI = "postgresql://user:FAKE_PASS@localhost:5432/demo_db"

# B108: Hardcoded /tmp path usage
log_file = "/tmp/app_debug.log"
