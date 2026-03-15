import os
import re
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

# Importing your custom library!
from indpy import is_pan, is_aadhaar

def extract_text_from_pdf(file_path: str) -> str:
    """Opens a PDF and extracts all readable text from its pages."""
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_image(file_path: str) -> str:
    """Opens an image and uses OCR to extract text."""
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error reading Image: {e}")
        return ""

def extract_identity_data(raw_text: str) -> dict:
    """Scans raw text and uses IndPy to validate Indian identity patterns."""
    data = {
        "pan_data": {"number": None, "is_valid": False},
        "aadhaar_data": {"number": None, "is_valid": False}
    }
    
    # 1. Find a potential PAN match in the text
    pan_pattern = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
    pan_match = re.search(pan_pattern, raw_text)
    
    if pan_match:
        potential_pan = pan_match.group(0)
        data["pan_data"]["number"] = potential_pan
        # Utilizing your indpy package to validate the extracted string
        data["pan_data"]["is_valid"] = is_pan(potential_pan) 
        
    # 2. Find a potential Aadhaar match in the text
    aadhaar_pattern = r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b'
    aadhaar_match = re.search(aadhaar_pattern, raw_text)
    
    if aadhaar_match:
        # Clean the string (remove spaces/hyphens) before passing to your library
        potential_aadhaar = re.sub(r'[\s\-]', '', aadhaar_match.group(0))
        data["aadhaar_data"]["number"] = potential_aadhaar
        # Utilizing your indpy package to validate the extracted string
        data["aadhaar_data"]["is_valid"] = is_aadhaar(potential_aadhaar)
        
    return data

def process_document(file_path: str, filename: str) -> dict:
    """Master function: Determines file type, extracts text, and finds IDs."""
    _, ext = os.path.splitext(filename)
    
    raw_text = ""
    
    # 1. Extract the text based on file extension
    if ext.lower() == ".pdf":
        raw_text = extract_text_from_pdf(file_path)
    elif ext.lower() in [".png", ".jpg", ".jpeg"]:
        raw_text = extract_text_from_image(file_path)
        
    # 2. Clean up the text (remove excessive newlines)
    clean_text = " ".join(raw_text.split())
    
    # 3. Find the identity data within the text
    extracted_data = extract_identity_data(clean_text)
    
    return {
        "text_found": bool(clean_text), 
        "extracted_data": extracted_data
    }