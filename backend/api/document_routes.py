from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
from pathlib import Path
from core.file_security import validate_file, generate_secure_filename
from core.extractor import process_document # <-- NEW IMPORT

router = APIRouter()

UPLOAD_DIR = Path("local_storage/pending_docs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        # 1. Validate & Secure
        validate_file(content_type=file.content_type, file_size=file.size)
        secure_name = generate_secure_filename(file.filename)
        file_path = UPLOAD_DIR / secure_name
        
        # 2. Save File
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 3. Extract Data (NEW LOGIC)
        # Convert Path object to string for the extractor
        extraction_results = process_document(str(file_path), secure_name)
            
        return {
            "original_filename": file.filename,
            "saved_as": secure_name,
            "status": "Success: File securely stored.",
            "document_analysis": extraction_results # <-- Return the extracted IDs
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while uploading.")