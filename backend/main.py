from fastapi import FastAPI
from api.document_routes import router as document_router

app = FastAPI(title="TrustGate API", description="Secure SME Onboarding Gateway")

# Register the document routes to the main application
app.include_router(document_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "TrustGate API is running securely."}