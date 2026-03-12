from fastapi import FastAPI


app = FastAPI(title="TrustGate API", description="Secure SME Onboarding Gateway")

@app.get("/")
async def root():
    return {"message": "Welcome to TrustGate API!"}

