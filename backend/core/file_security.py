import os
import uuid

# Define our strict security constraints
ALLOWED_MIME_TYPES = ["application/pdf", "image/jpeg", "image/png"]
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 Megabytes in bytes

def generate_secure_filename(original_filename: str) -> str:
    """Generates a random UUID filename while keeping the original extension."""
    # Extract the extension (e.g., '.pdf' from 'passport_scan.pdf')
    _, extension = os.path.splitext(original_filename)
    
    # Generate a random UUID and combine it with the extension
    secure_name = f"{uuid.uuid4()}{extension}"
    return secure_name

def validate_file(content_type: str, file_size: int):
    """Checks if the uploaded file meets our security criteria."""
    if content_type not in ALLOWED_MIME_TYPES:
        raise ValueError(f"Invalid file type. Allowed types: {', '.join(ALLOWED_MIME_TYPES)}")
        
    if file_size > MAX_FILE_SIZE:
        raise ValueError("File too large. Maximum size is 5MB.")