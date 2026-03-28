from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.document_routes import router as document_router
from core.config import FRONTEND_URL
from core.logger import logger

app = FastAPI(title="TrustGate API", description="Secure SME Onboarding Gateway")

logger.info("Starting TrustGate API")

# Create a robust list of allowed origins to prevent local browser blocking
origins = [
    FRONTEND_URL,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://0.0.0.0:5173/",
]

# Strip any accidental trailing slashes just to be safe
origins = [url.rstrip("/") for url in origins if url]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "TrustGate API is running securely."}