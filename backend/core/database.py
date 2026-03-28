import json
from datetime import datetime
from pathlib import Path
from core.config import DATABASE_PATH
from core.logger import logger

DB_FILE = Path(DATABASE_PATH)

def init_db() -> None:
    if not DB_FILE.exists():
        logger.info(f"Initializing new database at {DATABASE_PATH}")
        DB_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

def save_document_record(record: dict) -> None:
    init_db()

    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            logger.error("JSON Decode Error while reading database. Re-initializing.")
            data = []

    record["timestamp"] = datetime.now().isoformat()
    data.append(record)

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        logger.info(f"Saved document record for {record.get('saved_as', 'unknown')}")

def get_all_documents() -> list:
    init_db()

    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            logger.error("JSON Decode Error while reading database in get_all_documents.")
            return []

def delete_document_record(filename: str) -> bool:
    init_db()

    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            logger.error("JSON Decode Error while reading database in delete_document_record.")
            return False

    initial_length = len(data)
    updated_data = [record for record in data if record.get("saved_as") != filename]

    if len(updated_data) < initial_length:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(updated_data, f, indent=4)
        logger.info(f"Deleted document record: {filename}")
        return True

    return False
