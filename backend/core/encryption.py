import os
from cryptography.fernet import Fernet
from core.config import AES_MASTER_KEY
from core.logger import logger

def get_or_create_key() -> bytes:
    if AES_MASTER_KEY:
        return AES_MASTER_KEY.encode()
    else:
        logger.warning("AES_MASTER_KEY is not set in environment variables! Using fallback temporary key.")
        return Fernet.generate_key()

cipher_suite = Fernet(get_or_create_key())

def encrypt_data(file_bytes: bytes) -> bytes:
    try:
        return cipher_suite.encrypt(file_bytes)
    except Exception as e:
        logger.error(f"Encryption failed: {str(e)}")
        raise

def decrypt_data(encrypted_bytes: bytes) -> bytes:
    try:
        return cipher_suite.decrypt(encrypted_bytes)
    except Exception as e:
        logger.error(f"Decryption failed: {str(e)}")
        raise
