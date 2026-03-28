import os
import re
import fitz
import pytesseract
from PIL import Image
from indpy import is_pan, is_aadhaar
from core.logger import logger

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += str(page.get_text())
    except Exception as e:
        logger.error(f"Error reading PDF: {e}")
    return text

def extract_text_from_image(file_path: str) -> str:
    try:
        image = Image.open(file_path).convert('L')
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        logger.error(f"Error reading Image: {e}")
        return ""

def extract_identity_data(raw_text: str) -> dict:
    data = {
        "pan_data": {"number": None, "is_valid": False},
        "aadhaar_data": {"number": None, "is_valid": False}
    }

    pan_pattern = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
    pan_match = re.search(pan_pattern, raw_text)

    if pan_match:
        potential_pan = pan_match.group(0)
        data["pan_data"]["number"] = potential_pan
        data["pan_data"]["is_valid"] = is_pan(potential_pan)

    aadhaar_pattern = r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b'
    aadhaar_match = re.search(aadhaar_pattern, raw_text)

    if aadhaar_match:
        potential_aadhaar = re.sub(r'[\s\-]', '', aadhaar_match.group(0))
        data["aadhaar_data"]["number"] = potential_aadhaar
        data["aadhaar_data"]["is_valid"] = is_aadhaar(potential_aadhaar)

    return data

def process_document(file_path: str, filename: str) -> dict:
    _, ext = os.path.splitext(filename)
    raw_text = ""

    if ext.lower() == ".pdf":
        raw_text = extract_text_from_pdf(file_path)
    elif ext.lower() in [".png", ".jpg", ".jpeg"]:
        raw_text = extract_text_from_image(file_path)

    clean_text = " ".join(raw_text.split())
    extracted_data = extract_identity_data(clean_text)

    logger.info(f"Processed document {filename}. PAN: {extracted_data['pan_data']['is_valid']}, Aadhaar: {extracted_data['aadhaar_data']['is_valid']}")

    return {
        "text_found": bool(clean_text),
        "extracted_data": extracted_data
    }
