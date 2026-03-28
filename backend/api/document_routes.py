import mimetypes
from pathlib import Path
from fastapi import APIRouter, File, HTTPException, Response, UploadFile
from core.database import delete_document_record, get_all_documents, save_document_record
from core.encryption import decrypt_data, encrypt_data
from core.extractor import process_document
from core.file_security import generate_secure_filename, validate_file
from core.forgery_detector import analyze_image_forgery
from core.logger import logger

router = APIRouter()

UPLOAD_DIR = Path("local_storage/pending_docs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        raw_bytes = await file.read()
        validate_file(content_type=file.content_type, file_size=len(raw_bytes))

        secure_name = generate_secure_filename(file.filename)
        file_path = UPLOAD_DIR / secure_name

        with open(file_path, "wb") as buffer:
            buffer.write(raw_bytes)

        security_scan = analyze_image_forgery(str(file_path))
        extraction_results = process_document(str(file_path), secure_name)

        encrypted_bytes = encrypt_data(raw_bytes)
        with open(file_path, "wb") as buffer:
            buffer.write(encrypted_bytes)

        final_result = {
            "original_filename": file.filename,
            "saved_as": secure_name,
            "status": "Success: File securely stored and AES-encrypted.",
            "document_analysis": extraction_results,
            "security_scan": security_scan,
        }

        save_document_record(final_result)
        logger.info(f"Successfully processed and encrypted document: {secure_name}")
        return final_result
    except ValueError as e:
        logger.warning(f"Validation failed for upload: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error during upload_document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/documents")
async def fetch_all_documents():
    try:
        records = get_all_documents()
        logger.info("Fetched all document records")
        return {"total_records": len(records), "data": records}
    except Exception as e:
        logger.error(f"Failed to fetch database records: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch database records.")

@router.delete("/documents/{filename}")
async def delete_document(filename: str):
    try:
        file_path = UPLOAD_DIR / filename
        file_deleted = False

        if file_path.exists():
            file_path.unlink()
            file_deleted = True

        record_deleted = delete_document_record(filename)

        if not file_deleted and not record_deleted:
            logger.warning(f"Delete requested for missing document: {filename}")
            raise HTTPException(status_code=404, detail="Document not found.")

        logger.info(f"Successfully deleted document: {filename}")
        return {"status": "success", "message": f"Document {filename} permanently securely deleted."}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete document {filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")

@router.get("/documents/{filename}/view")
async def view_secure_document(filename: str):
    try:
        file_path = UPLOAD_DIR / filename
        if not file_path.exists():
            logger.warning(f"View requested for missing document: {filename}")
            raise HTTPException(status_code=404, detail="Secure document not found.")

        with open(file_path, "rb") as locked_file:
            encrypted_bytes = locked_file.read()

        decrypted_bytes = decrypt_data(encrypted_bytes)
        media_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        
        logger.info(f"Successfully decrypted and served document: {filename}")
        return Response(content=decrypted_bytes, media_type=media_type)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to decrypt document {filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to decrypt document: {str(e)}")
