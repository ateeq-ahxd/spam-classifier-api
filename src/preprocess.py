# ============================================================
# 🧹 TEXT PREPROCESSING
# Cleans raw email text before feeding to the model
# ============================================================

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK data (only happens once)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet',   quiet=True)

# Initialize lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words  = set(stopwords.words('english'))


def clean_text(text: str) -> str:
    """
    Takes raw email text and cleans it step by step.
    Returns cleaned string ready for TF-IDF vectorizer.
    """

    # Step 1: Make everything lowercase
    # "FREE" and "free" are the same word
    text = text.lower()

    # Step 2: Remove email addresses
    # "john@gmail.com" adds no meaning
    text = re.sub(r'\S+@\S+', '', text)

    # Step 3: Remove URLs
    # "http://spam.com" adds no meaning
    text = re.sub(r'http\S+|www\S+', '', text)

    # Step 4: Remove "Subject:" prefix
    # Every email starts with this — not useful
    text = re.sub(r'subject:', '', text)

    # Step 5: Remove numbers
    # "1000" "2024" not useful for text analysis
    text = re.sub(r'\d+', '', text)

    # Step 6: Remove special characters
    # Keep only letters and spaces
    text = re.sub(r'[^a-z\s]', '', text)

    # Step 7: Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # Step 8: Remove stopwords and lemmatize
    # "the", "is", "at" add no meaning
    # "running" → "run", "prices" → "price"
    tokens = [
        lemmatizer.lemmatize(word)
        for word in text.split()
        if word not in stop_words
        and len(word) > 2
    ]

    return " ".join(tokens) 
