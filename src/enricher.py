# ============================================================
# 🎭 RESPONSE ENRICHER
# Adds personality, roast, GIF and threat analysis
# ============================================================

import re
import random
import httpx
import os
from dotenv import load_dotenv

load_dotenv()


# ── Spam personality types ───────────────────────────────────
# Each type has keywords to detect it, and a GIF search term

PERSONALITIES = {
    "nigerian_prince": {
        "name"    : "The Aristocrat",
        "desc"    : "A deposed royal needs YOUR help moving millions. Discretion advised.",
        "keywords": ["prince", "million", "transfer", "inheritance", "confidential"],
        "giphy"   : "suspicious side eye"
    },
    "lottery_winner": {
        "name"    : "The Lucky One",
        "desc"    : "Congratulations! You won a competition you never entered. Remarkable.",
        "keywords": ["winner", "lottery", "prize", "congratulations", "selected", "award"],
        "giphy"   : "yeah right not buying it"
    },
    "urgent_larry": {
        "name"    : "Urgent Larry",
        "desc"    : "Everything is on fire. Reply in 4 minutes or lose everything forever.",
        "keywords": ["urgent", "immediately", "act now", "limited time", "expires", "final notice"],
        "giphy"   : "everything is fine fire"
    },
    "pharma_bro": {
        "name"    : "The Unlicensed Pharmacist",
        "desc"    : "Deeply concerned about your health. Conveniently selling solutions.",
        "keywords": ["pill", "viagra", "medication", "pharmacy", "prescription", "weight loss"],
        "giphy"   : "no thanks doctor"
    },
    "link_goblin": {
        "name"    : "The Link Distributor",
        "desc"    : "Has many URLs to share. None of them are what they claim to be.",
        "keywords": ["click here", "visit", "http", "www", "link", "subscribe"],
        "giphy"   : "suspicious link do not click"
    },
    "too_good": {
        "name"    : "The Deal of a Lifetime",
        "desc"    : "An offer so generous it only needs your bank details and full trust.",
        "keywords": ["free", "discount", "offer", "deal", "save", "percent off", "coupon"],
        "giphy"   : "too good to be true"
    },
    "account_alert": {
        "name"    : "The Concerned Institution",
        "desc"    : "Your bank needs verification. Your bank does not know this email exists.",
        "keywords": ["account", "verify", "password", "login", "suspended", "bank", "paypal"],
        "giphy"   : "phishing scam caught"
    },
}


# ── Roast lines ──────────────────────────────────────────────
# 6 roasts per personality → picked randomly each time
# Dry, witty, professor-safe humour

ROASTS = {
    "nigerian_prince": [
        "The geopolitical situation described is entirely fictional. So is the money.",
        "A prince with $47M and no bank account. Plausible.",
        "Written with the confidence of someone who has never met a bank.",
        "The prince has been trying to move this money since 2003. Still at it.",
        "Geographically creative. Financially suspect.",
        "A masterclass in financial fiction. Points for commitment.",
    ],
    "lottery_winner": [
        "You won a competition you never entered. Remarkable odds.",
        "The prize is real. The sender's address is not.",
        "Winning has never looked this unconvincing.",
        "The odds of winning a lottery you never entered remain statistically low.",
        "A celebration in search of a victim.",
        "Congratulations are premature. As is clicking anything here.",
    ],
    "urgent_larry": [
        "The countdown timer exists only in the sender's imagination.",
        "FINAL NOTICE. For the fourth time this week.",
        "Everything is urgent when you have nothing credible to say.",
        "Panic is the intended response. Deletion is the correct one.",
        "A time-sensitive offer with a 20-year shelf life.",
        "The urgency is manufactured. The threat is not.",
    ],
    "pharma_bro": [
        "Peer-reviewed this is not.",
        "No medical board has endorsed this email. Shockingly.",
        "The prescription pad is unlicensed. So is everything else.",
        "Deeply invested in your wellbeing. Financially.",
        "The side effects include identity theft and regret.",
        "A pharmaceutical mystery with a known ending.",
    ],
    "link_goblin": [
        "A generous distribution of URLs, none of them trustworthy.",
        "The links go somewhere. That somewhere is not what they claim.",
        "URL shorteners: for when your destination needs to be a surprise.",
        "Redirects all the way down.",
        "Clicks requested. Judgment recommended instead.",
        "The hyperlinks are working as intended. That is the problem.",
    ],
    "too_good": [
        "Economics does not support this proposition.",
        "The fine print does not exist. Neither does the offer.",
        "A deal structured entirely in the sender's favour.",
        "Priced at free. Valued accordingly.",
        "The generous offer requires only your complete personal history.",
        "An arrangement this generous typically has no fine print because there is no deal.",
    ],
    "account_alert": [
        "Your bank communicates via this domain. It does not.",
        "A very convincing logo. A very unconvincing email.",
        "The institution named was not consulted in making this email.",
        "Security concerns raised by the least secure email you will receive today.",
        "The real alert is this email itself.",
        "Verification requested by someone other than who they claim to be.",
    ],
    "general_spam": [
        "The model has seen enough.",
        "Not subtle. Not effective. Definitely spam.",
        "A textbook case study in what not to send.",
        "Flagged with minimal deliberation.",
        "The signals here are not mixed.",
        "Confidence: high. Legitimacy: low.",
    ],
    "clean_email": [
        "Cleared for landing.",
        "The model finds no cause for alarm. Proceed with reasonable caution.",
        "Against all odds, this one seems fine.",
        "No red flags detected. The bar was low but this clears it.",
        "Statistically, some emails are legitimate. This appears to be one.",
        "Nothing flagged. Either genuine or very well written spam.",
    ],
}


# ── Helper functions ─────────────────────────────────────────

def detect_personality(text: str) -> str:
    """Checks email text against each personality's keywords."""
    text_lower = text.lower()
    for key, data in PERSONALITIES.items():
        if any(kw in text_lower for kw in data["keywords"]):
            return key
    return "general_spam"


def extract_links(text: str) -> list:
    """Finds all URLs in the email."""
    return re.findall(r'https?://\S+|www\.\S+', text)


def extract_flagged_words(text: str) -> list:
    """Finds known spam words present in the email."""
    spam_lexicon = [
        "free", "win", "winner", "prize", "urgent", "act now",
        "click", "offer", "limited", "expires", "guaranteed",
        "cash", "money", "credit", "loan", "viagra", "pill",
        "discount", "save", "deal", "congratulations", "selected",
        "password", "verify", "account", "suspended", "confirm",
        "bank", "transfer", "million", "inheritance"
    ]
    text_lower = text.lower()
    return list({w for w in spam_lexicon if w in text_lower})


def compute_threat_scores(text: str) -> dict:
    """Returns 4 threat sub-scores as percentages."""
    words = text.lower().split()
    total = max(len(words), 1)

    urgency_kw = [
        "urgent", "now", "immediately", "expires",
        "limited", "final", "act", "hurry", "deadline"
    ]

    # ✅ FIXED — matches flagged_words lexicon so scores are consistent
    scam_kw = [
        "free", "win", "winner", "prize", "money", "cash",
        "million", "guaranteed", "congratulations", "selected",
        "inheritance", "transfer", "loan", "credit", "offer",
        "discount", "deal", "save"
    ]

    urgency = round(min(
        sum(1 for w in words if w in urgency_kw) / total * 500, 100
    ))
    scam = round(min(
        sum(1 for w in words if w in scam_kw) / total * 500, 100
    ))
    caps = round(min(
        sum(1 for c in text if c.isupper()) / max(len(text), 1) * 300, 100
    ))
    links = min(len(extract_links(text)) * 25, 100)

    return {
        "scam_words"       : scam,
        "urgency_signals"  : urgency,
        "caps_abuse"       : caps,
        "suspicious_links" : links
    }


async def get_gif(search_term: str):
    """Fetches a random GIF from GIPHY matching the search term."""
    try:
        key = os.getenv("GIPHY_API_KEY", "")

        # Skip if no key set
        if not key or key == "your_giphy_key_here":
            return None

        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                "https://api.giphy.com/v1/gifs/search",
                params={
                    "api_key": key,
                    "q"      : search_term,
                    "limit"  : 10,
                    "rating" : "pg"
                }
            )

        gifs = response.json().get("data", [])

        if not gifs:
            return None

        # Pick randomly from 10 results → never same GIF twice!
        chosen = random.choice(gifs)
        return chosen["images"]["original"]["url"]

    except Exception:
        # ✅ FIXED — Giphy failure never crashes the app
        return None


async def enrich(text: str, is_spam: bool) -> dict:
    """
    Main enrichment function.
    Builds the full rich response on top of the model prediction.
    """

    if not is_spam:
        # Clean email — different personality and roast pool
        personality_key  = "clean_email"
        personality_data = {
            "name" : "Looks Legit",
            "desc" : "Nothing suspicious detected. You may proceed with your day.",
            "giphy": "thumbs up all good"
        }
    else:
        # Detect which spam personality this is
        personality_key  = detect_personality(text)

        # ✅ FIXED — fallback no longer uses link_goblin data for general_spam
        personality_data = PERSONALITIES.get(
            personality_key,
            {
                "name" : "Suspicious Character",
                "desc" : "Flagged by the model. No specific personality matched.",
                "giphy": "suspicious"
            }
        )

    # Pick random roast from the pool
    roast = random.choice(
        ROASTS.get(personality_key, ROASTS["general_spam"])
    )

    # Fetch GIF from GIPHY — safe, never crashes
    gif_url = await get_gif(personality_data["giphy"])

    return {
        "personality_type" : personality_key,
        "personality_name" : personality_data["name"],
        "personality_desc" : personality_data["desc"],
        "roast"            : roast,
        "gif_url"          : gif_url,
        "flagged_words"    : extract_flagged_words(text) if is_spam else [],
        "links_found"      : extract_links(text),
        "threat_scores"    : compute_threat_scores(text) if is_spam else {},
        "user_can_override": True
    }