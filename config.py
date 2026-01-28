# import os
# from dotenv import load_dotenv

# load_dotenv()

# DB_HOST = "localhost"
# DB_USER = "root"
# DB_PASSWORD = "Sownd@05"
# DB_NAME = "pastebin"

# TEST_MODE = os.getenv("TEST_MODE") == "1"


import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# PostgreSQL configuration
DB_HOST = os.getenv("DB_HOST", "localhost")      # Use environment variable, default localhost
DB_USER = os.getenv("DB_USER", "postgres")       # Default postgres user
DB_PASSWORD = os.getenv("DB_PASSWORD", "Sownd@05")  # Replace with your PostgreSQL password
DB_NAME = os.getenv("DB_NAME", "pastedb")       # Database name
DB_PORT = int(os.getenv("DB_PORT", 5432))       # PostgreSQL default port

# Optional: test mode
TEST_MODE = os.getenv("TEST_MODE") == "1"

