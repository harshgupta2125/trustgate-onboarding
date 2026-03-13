from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
from pathlib import Path
from core.file_security import validate_file, generate_secure_filename

router = APIRouter()

# Ensure the physical directory exists where we will save files
UPLOAD_DIR = Path("local_storage/pending_docs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        # 1. Validate the file before processing it further
        validate_file(content_type=file.content_type, file_size=file.size)
        
        # 2. Generate a secure, randomized filename
        secure_name = generate_secure_filename(file.filename)
        
        # 3. Create the exact destination path
        file_path = UPLOAD_DIR / secure_name
        
        # 4. Open a new file on disk and securely stream the uploaded data into it
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {
            "original_filename": file.filename,
            "saved_as": secure_name,
            "status": "Success: File securely stored."
        }
        
    except ValueError as e:
        # Catch our custom validation errors (wrong type/too large)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Catch any other unexpected server errors
        raise HTTPException(status_code=500, detail="An error occurred while uploading.")