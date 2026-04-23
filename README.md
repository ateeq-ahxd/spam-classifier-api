# Spam Classifier API

A production-ready spam detection API built with FastAPI and Scikit-learn. Accepts raw email text and returns a classification verdict, confidence score, threat signal breakdown, and flagged trigger words — all over a clean REST interface.

Live: `spam-classifier-api-production-b951.up.railway.app`  
Docs: `spam-classifier-api-production-b951.up.railway.app/docs`

---

## Overview

This project was built as part of a capstone in data analytics and extended into a deployable API. The classifier uses a TF-IDF vectorizer paired with an SVM model trained on a labelled email dataset. The API wraps the model with additional signal analysis — urgency detection, caps abuse scoring, suspicious link presence — to give a richer picture of why an email was flagged, not just whether it was.

---

## Features

- **ML classification** — TF-IDF + SVM pipeline, serialised with joblib and loaded at startup
- **Confidence scoring** — probability output alongside the binary verdict
- **Threat signal breakdown** — scam keyword density, urgency signal count, caps ratio, suspicious link detection
- **Flagged word extraction** — exact tokens that contributed to the classification
- **User override** — endpoint accepts a correction flag for downstream feedback loops
- **GIF response layer** — optional Giphy integration for client-facing UI (can be disabled)

---

## API Reference

### `POST /predict`

Classifies a single email as spam or legitimate.

**Request**
```json
{
  "email_text": "CONGRATULATIONS! You have WON $1,000,000! Click NOW!"
}
```

**Response**
```json
{
  "verdict": "SPAM",
  "confidence": 97.4,
  "flagged_words": ["CONGRATULATIONS", "WON", "Click NOW"],
  "threat_scores": {
    "scam_words": 88,
    "urgency_signals": 91,
    "caps_abuse": 75,
    "suspicious_links": 0
  },
  "links_found": [],
  "user_can_override": true
}
```

| Field | Type | Description |
|---|---|---|
| `verdict` | string | `SPAM` or `HAM` |
| `confidence` | float | Model confidence as a percentage |
| `flagged_words` | array | Tokens that triggered classification |
| `threat_scores` | object | Per-signal scores, 0–100 |
| `user_can_override` | bool | Whether the client can submit a correction |

---

## Tech Stack

| Layer | Technology |
|---|---|
| API framework | FastAPI |
| ML model | Scikit-learn — SVM |
| Text processing | TF-IDF vectorizer, NLTK |
| Serialisation | joblib |
| GIF integration | Giphy API (optional) |
| Deployment | Railway |
| Language | Python 3.11+ |

---

## Running Locally

**Prerequisites:** Python 3.11+, pip

```bash
git clone https://github.com/ateeq-ahxd/spam-classifier-api.git
cd spam-classifier-api

pip install -r requirements.txt

cp .env.example .env
# Add your API keys to .env

uvicorn main:app --reload
```

Interactive docs available at `http://127.0.0.1:8000/docs`

---

## Environment Variables

| Variable | Description |
|---|---|
| `GIPHY_API_KEY` | Giphy API key for GIF responses |
| `MODEL_PATH` | Local path to the trained model `.pkl` |
| `TFIDF_PATH` | Local path to the TF-IDF vectorizer `.pkl` |
| `MODEL_GDRIVE_ID` | Google Drive file ID — used if model is hosted remotely |
| `TFIDF_GDRIVE_ID` | Google Drive file ID — used if vectorizer is hosted remotely |

---

## Model Performance

Evaluated on a held-out test set of 1,115 emails.

| Metric | Score |
|---|---|
| Accuracy | 99.5% |
| Spam Precision | 97.3% |
| Spam Recall | 98.6% |
| F1-Score | 97.9% |

Confusion matrix: 965 true ham, 144 true spam, 4 false positives, 2 false negatives.

---

## Project Background

Built as a capstone project for a data analytics programme and extended into a fully deployed API. The core model was developed collaboratively by a six-person team (Team 404). The API layer, deployment, and additional signal analysis were built independently as a portfolio extension.

---

## Roadmap

- [ ] Batch prediction endpoint — classify multiple emails per request
- [ ] SHAP integration — token-level explanation of model decisions
- [ ] Multi-language support — extend beyond English training data
- [ ] Feedback loop — store user overrides to retrain on corrections
- [ ] Gmail / Outlook plugin — real inbox integration

---

*Built by Ateeq — open to feedback and contributions.*
