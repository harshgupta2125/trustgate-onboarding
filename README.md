# TrustGate: Secure SME Onboarding Gateway

TrustGate is a self-hosted, full-stack compliance application designed to help businesses securely collect, validate, and manage sensitive client identity documents. It goes beyond basic file uploading by implementing enterprise-grade security protocols and Machine Learning-based forgery detection.

## 🚀 The Problem It Solves
Handling highly sensitive documents (PAN, Aadhaar) insecurely via email or standard web forms is a massive liability. TrustGate provides a secure local portal where documents are uploaded, automatically scanned for structural compliance, checked for digital tampering, and immediately locked in an AES-256 encrypted vault.

## 🧠 Enterprise Features
* **The Zero-Trust Vault (AES-256):** Uploaded documents are encrypted *in memory* before being written to the file system. The physical files are unreadable ciphertext to anyone browsing the server.
* **On-the-Fly Decryption Streaming:** Authorized admins can view the documents via a secure backend route that decrypts the file in memory and streams it directly to the React frontend without leaving decrypted traces on the hard drive.
* **Machine Learning Forgery Detection:** Utilizes OpenCV and Error Level Analysis (ELA) to scan pixel compression signatures, calculating a "Tamper Risk Score" to instantly flag digitally altered or Photoshopped ID cards.
* **Custom Open-Source Validation:** Directly integrates my published PyPI package, **`indpy`**, to rigorously validate extracted Indian identity formats (PAN/Aadhaar) using advanced regex and checksum logic.
* **DPDP/GDPR Compliance:** Features a "Purge" function that permanently deletes both the encrypted file and the database record.

## 🛠️ Tech Stack
* **Frontend:** React (Vite), JavaScript, CSS
* **Backend:** Python, FastAPI, Uvicorn
* **Data Extraction & ML:** Tesseract OCR, PyMuPDF, OpenCV, NumPy
* **Security:** Cryptography (Fernet AES-256)
* **Validation Engine:** `indpy` (Custom PyPI Library)
* **Database:** Robust JSON Flat-file System

## 🚦 How to Run Locally

### 1. Backend Setup
Navigate to the backend directory, install dependencies, and start the FastAPI server:
```bash
cd backend
uv sync # Or use: pip install -r requirements.txt
uv run uvicorn main:app --reload
```
*(The backend runs on http://localhost:8000)*

### 2. Frontend Setup
Open a new terminal, navigate to the frontend directory, and start the Vite development server:
```bash
cd frontend
npm install
npm run dev
```
*(The frontend runs on http://localhost:5173)*

## 🔐 Configuration (Optional)
If you are moving strings to production, ensure you generate and set a permanent `ENCRYPTION_KEY` in the backend so your files remain consistently decryptable across server restarts:
```bash
export ENCRYPTION_KEY="your-secure-base64-fernet-key"
```

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Check out the [issues page](https://github.com/harshgupta2125/trustgate-onboarding/issues) to get started.

## 📜 License
This project is open-source and available under the MIT License.
