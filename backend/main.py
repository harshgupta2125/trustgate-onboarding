from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # NEW IMPORT
from api.document_routes import router as document_router

app = FastAPI(title="TrustGate API", description="Secure SME Onboarding Gateway")

# NEW CORS CONFIGURATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], # Allow your Vite app
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers
)

app.include_router(document_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "TrustGate API is running securely."}