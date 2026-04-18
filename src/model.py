# ============================================================
# 🤖 MODEL LOADER AND PREDICTOR
# Loads saved model files and makes predictions
# ============================================================

import joblib
import pickle
import numpy as np
import os
from dotenv import load_dotenv
from src.preprocess import clean_text

# Load environment variables from .env file
load_dotenv()


# ── Load model files ONCE at startup ────────────────────────
# Loading inside predict() would be slow — once is enough!

print("⏳ Loading model files...")

# Load TF-IDF vectorizer
tfidf_path = os.getenv("TFIDF_PATH", "models/tfidf_vectorizer.pkl")
tfidf = joblib.load(tfidf_path)

# Load trained classifier
model_path = os.getenv("MODEL_PATH", "models/spam_model.pkl")
model = joblib.load(model_path)

print("✅ Models loaded successfully!")


# ── Prediction function ──────────────────────────────────────

def predict(text: str) -> dict:
    """
    Takes raw email text and returns prediction.

    Args:
        text: raw email string

    Returns:
        dict with is_spam, verdict, confidence
    """

    # Step 1: Clean the text
    cleaned = clean_text(text)

    # Step 2: Convert to TF-IDF numbers
    vectorized = tfidf.transform([cleaned])

    # Step 3: Get prediction (0=ham, 1=spam)
    prediction = model.predict(vectorized)[0]

    # Step 4: Get confidence percentage
    # predict_proba returns [prob_ham, prob_spam]
    probability = model.predict_proba(vectorized)[0]
    confidence  = round(float(np.max(probability)) * 100, 1)

    return {
        "is_spam"   : bool(prediction == 1),
        "verdict"   : "SPAM" if prediction == 1 else "HAM",
        "confidence": confidence
    }