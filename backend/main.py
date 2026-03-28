from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.document_routes import router as document_router
from core.config import FRONTEND_URL
from core.logger import logger

app = FastAPI(title="TrustGate API", description="Secure SME Onboarding Gateway")

logger.info("Starting TrustGate API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "TrustGate API is running securely."}