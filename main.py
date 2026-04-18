# ============================================================
# 🚀 MAIN FASTAPI APPLICATION
# Entry point — runs the API server
# ============================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.model    import predict
from src.enricher import enrich

# Create the FastAPI app
app = FastAPI(
    title       = "Spam Classifier API",
    description = "Spam detection with personality type, roast and GIF",
    version     = "1.0.0"
)

# Allow frontend to talk to this backend
# CORS = Cross Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins  = ["*"],   # any frontend can connect
    allow_methods  = ["*"],
    allow_headers  = ["*"],
)


# ── Request model ────────────────────────────────────────────
# Defines what the frontend must send us

class EmailRequest(BaseModel):
    email_text: str


# ── Routes ───────────────────────────────────────────────────

@app.get("/")
def root():
    """Basic check that server is running."""
    return {"message": "Spam Classifier API is running!"}


@app.get("/health")
def health():
    """Health check for Render deployment monitoring."""
    return {"status": "alive"}


@app.post("/predict")
async def predict_email(req: EmailRequest):
    """
    Main prediction endpoint.
    Receives email text → returns full analysis.
    """

    # Validate input
    if not req.email_text.strip():
        raise HTTPException(
            status_code = 400,
            detail      = "Email text cannot be empty"
        )

    if len(req.email_text) > 50000:
        raise HTTPException(
            status_code = 400,
            detail      = "Email too long — max 50,000 characters"
        )

    # Get model prediction
    result = predict(req.email_text)

    # Get enriched response (personality, roast, GIF etc.)
    extras = await enrich(req.email_text, result["is_spam"])

    # Merge and return everything
    return {**result, **extras}
