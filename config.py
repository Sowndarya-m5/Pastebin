import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Sownd@05"
DB_NAME = "pastebin"

TEST_MODE = os.getenv("TEST_MODE") == "1"
