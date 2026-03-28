import os
import uuid

ALLOWED_MIME_TYPES = ["application/pdf", "image/jpeg", "image/png"]
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 Megabytes in bytes

def generate_secure_filename(original_filename: str) -> str:
    _, extension = os.path.splitext(original_filename)
    secure_name = f"{uuid.uuid4()}{extension}"
    return secure_name

def validate_file(content_type: str, file_size: int):
    if content_type not in ALLOWED_MIME_TYPES:
        raise ValueError(f"Invalid file type. Allowed types: {', '.join(ALLOWED_MIME_TYPES)}")
    if file_size > MAX_FILE_SIZE:
        raise ValueError("File is too large. Maximum size is 5MB.")
