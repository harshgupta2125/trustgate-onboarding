import os
from dotenv import load_dotenv

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
AES_MASTER_KEY = os.getenv("AES_MASTER_KEY")
DATABASE_PATH = os.getenv("DATABASE_PATH", "local_storage/database.json")
