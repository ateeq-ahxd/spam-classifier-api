# 🛡️ Spam Classifier API

> A fun, intelligent spam detection API built with FastAPI and Machine Learning.
> Not just "spam or not" — it roasts the email, gives it a personality, and
> tells you exactly why it's suspicious. Built as a portfolio project.

---

## ✨ Features

- 🧠 **ML-powered** spam detection using TF-IDF + Scikit-learn
- 😂 **Spam Personalities** — Nigerian Prince, Urgent Larry, Link Goblin & more
- 🔥 **Roast Mode** — savage one-liner about why the email is sus
- 📊 **Threat Breakdown** — scam words, urgency signals, caps abuse, suspicious links
- 🎭 **Reaction GIFs** — powered by Giphy API
- 🚩 **Flagged Words** — exact words that triggered the model
- ✅ **User Override** — because models aren't always right

---

## 🚀 Live API

spam-classifier-api-production-b951.up.railway.app

Full interactive docs:

---

## 📡 API Usage

### POST /predict

**Request:**
```json
{
  "email_text": "CONGRATULATIONS! You have WON $1,000,000! Click NOW!"
}
```

**Response:**
```json
{
  "verdict": "SPAM",
  "confidence": 97.4,
  "personality_name": "Urgent Larry",
  "personality_desc": "Everything is on fire. Reply NOW or lose everything.",
  "roast": "The countdown timer exists only in your imagination.",
  "gif_url": "https://media.giphy.com/...",
  "flagged_words": ["CONGRATULATIONS", "WON", "Click NOW"],
  "links_found": [],
  "threat_scores": {
    "scam_words": 88,
    "urgency_signals": 91,
    "caps_abuse": 75,
    "suspicious_links": 0
  },
  "user_can_override": true
}
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| ML Model | Scikit-learn (Naive Bayes / SVM) |
| Text Processing | NLTK + TF-IDF |
| GIF Integration | Giphy API |
| Deployment | Railway | Render
| Language | Python 3.14 |

---

## 🏃 Run Locally

```bash
# Clone the repo
git clone https://github.com/ateeq-ahxd/spam-classifier-api.git
cd spam-classifier-api

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Fill in your API keys

# Run the server
uvicorn main:app --reload
```

Then open: http://127.0.0.1:8000/docs

---

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GIPHY_API_KEY` | Your Giphy API key |
| `MODEL_PATH` | Path to spam model pkl file |
| `TFIDF_PATH` | Path to TF-IDF vectorizer pkl file |
| `MODEL_GDRIVE_ID` | Google Drive ID for model file |
| `TFIDF_GDRIVE_ID` | Google Drive ID for vectorizer file |

---

## 👨‍💻 Author

Built as a first portfolio project
⭐ Star this repo if you found it useful!
