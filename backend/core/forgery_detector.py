import cv2
import numpy as np
import os
from core.logger import logger

def analyze_image_forgery(file_path: str) -> dict:
    try:
        original = cv2.imread(file_path)
        if original is None:
            logger.warning(f"Failed to read image for ELA: {file_path}")
            return {"is_forged": False, "suspicion_score": 0, "status": "Failed to read image for ELA"}
            
        temp_path = file_path + ".temp.jpg"
        cv2.imwrite(temp_path, original, [cv2.IMWRITE_JPEG_QUALITY, 90])

        compressed = cv2.imread(temp_path)

        if os.path.exists(temp_path):
            os.remove(temp_path)

        diff = cv2.absdiff(original, compressed)
        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        
        variance = np.var(gray_diff)
        score = round(min(variance * 2, 100), 2)
        is_forged = bool(score > 40.0)

        if is_forged:
            logger.warning(f"High Tampering Probability detected for {file_path}. Score: {score}")

        return {
            "is_forged": is_forged,
            "suspicion_score": score,
            "status": "Warning: High Tampering Probability" if is_forged else "Passed ELA Check"
        }

    except Exception as e:
        logger.error(f"ELA Engine Error on {file_path}: {e}")
        return {"is_forged": False, "suspicion_score": 0.0, "status": "Error running ELA"}
