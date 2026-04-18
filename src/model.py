# ============================================================
# 🤖 MODEL LOADER AND PREDICTOR
# Loads saved model files and makes predictions
# ============================================================

import joblib
import numpy as np
import os
import gdown
from dotenv import load_dotenv
from src.preprocess import clean_text

# Load environment variables from .env file
load_dotenv()


# ── Download models from Google Drive if not present ────────
def download_if_missing():
    os.makedirs("models", exist_ok=True)

    if not os.path.exists("models/spam_model.pkl"):
        print("⏳ Downloading model from Google Drive...")
        gdown.download(
            f"https://drive.google.com/uc?id={os.getenv('MODEL_GDRIVE_ID')}",
            "models/spam_model.pkl",
            quiet=False
        )
        print("✅ Model downloaded!")

    if not os.path.exists("models/tfidf_vectorizer.pkl"):
        print("⏳ Downloading vectorizer from Google Drive...")
        gdown.download(
            f"https://drive.google.com/uc?id={os.getenv('TFIDF_GDRIVE_ID')}",
            "models/tfidf_vectorizer.pkl",
            quiet=False
        )
        print("✅ Vectorizer downloaded!")

# Run download on startup
download_if_missing()


# ── Load model files ONCE at startup ────────────────────────
print("⏳ Loading model files...")

tfidf_path = os.getenv("TFIDF_PATH", "models/tfidf_vectorizer.pkl")
tfidf = joblib.load(tfidf_path)

model_path = os.getenv("MODEL_PATH", "models/spam_model.pkl")
model = joblib.load(model_path)

print("✅ Models loaded successfully!")


# ── Prediction function ──────────────────────────────────────
def predict(text: str) -> dict:
    cleaned    = clean_text(text)
    vectorized = tfidf.transform([cleaned])
    prediction = model.predict(vectorized)[0]
    probability = model.predict_proba(vectorized)[0]
    confidence  = round(float(np.max(probability)) * 100, 1)

    return {
        "is_spam"   : bool(prediction == 1),
        "verdict"   : "SPAM" if prediction == 1 else "HAM",
        "confidence": confidence
    }