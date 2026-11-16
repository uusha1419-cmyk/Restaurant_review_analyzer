import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from transformers import pipeline

app = FastAPI(title="Restaurant Review Analyzer API")

# Load the pre-trained Hugging Face model once at startup
sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
)

CATEGORY_KEYWORDS = {
    "food": {"food", "dish", "meal", "taste", "pasta", "pizza", "burger", "sauce",
             "dessert", "cooked", "fresh", "cold", "bland", "delicious", "tasty", "menu"},
    "service": {"service", "staff", "waiter", "waitress", "server", "manager",
                "rude", "friendly", "ignored", "helpful", "polite"},
    "cleanliness": {"clean", "dirty", "filthy", "hygiene", "messy", "spotless",
                    "tables", "table", "floor", "restroom", "bathroom"},
    "waiting_time": {"wait", "waited", "waiting", "slow", "fast", "quick",
                     "minutes", "hour", "hours", "long", "delay", "delayed"},
}

SAMPLE_REVIEWS = [
    "The pasta was amazing! Sauce was rich and perfectly cooked. But our waiter was rude and we waited 40 minutes.",
    "Absolutely loved everything. Staff were friendly, food came fast, and the dessert was heavenly!",
    "Disappointing visit. Tables were dirty, food was cold, and staff completely ignored us.",
    "Decent food but nothing special. Service was average, place was clean.",
    "Great pizza and quick service. The restaurant was spotless.",
    "We waited an hour and the food was bland. Never coming back.",
]


class ReviewRequest(BaseModel):
    review: str

    @field_validator("review")
    @classmethod
    def validate_review(cls, v):
        if not v or not v.strip():
            raise ValueError("Review text cannot be empty")
        if len(v) > 2000:
            raise ValueError("Review text too long (max 2000 characters)")
        return v.strip()


def split_sentences(text):
    parts = re.split(r"(?<=[.!?])\s+|\s+but\s+", text, flags=re.IGNORECASE)
    return [p.strip() for p in parts if p.strip()]


def category_sentiments(text):
    sentences = split_sentences(text)

    # Find which categories each sentence talks about
    matches = []
    for s in sentences:
        words = set(re.findall(r"[a-z]+", s.lower()))
        cats = {c for c, kw in CATEGORY_KEYWORDS.items() if kw & words}
        if len(cats) > 1:
            cats.discard("food")   # "food" is a generic word, so prefer the specific category
        matches.append((s, cats))

    results = {}
    for cat in CATEGORY_KEYWORDS:
        matched = [s for s, cats in matches if cat in cats]
        if not matched:
            results[cat] = "neutral"
            continue
        preds = sentiment_model(matched, truncation=True)
        score = sum(1 if p["label"] == "POSITIVE" else -1 for p in preds)
        results[cat] = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    return results

def make_summary(sentiment, cats):
    pos = [c.replace("_", " ") for c, s in cats.items() if s == "positive"]
    neg = [c.replace("_", " ") for c, s in cats.items() if s == "negative"]
    parts = []
    if pos:
        parts.append("Positive about " + ", ".join(pos))
    if neg:
        parts.append("Negative about " + ", ".join(neg))
    if parts:
        return ". ".join(parts) + "."
    return f"Overall {sentiment.lower()} review with no specific category mentioned."


def analyze(text):
    result = sentiment_model(text, truncation=True)[0]
    sentiment = result["label"] if result["score"] >= 0.60 else "NEUTRAL"
    cats = category_sentiments(text)
    return {
        "review": text,
        "sentiment": sentiment,
        "confidence": round(result["score"] * 100, 1),
        "summary": make_summary(sentiment, cats),
        "categories": cats,
    }


@app.post("/analyze_review")
def analyze_review(request: ReviewRequest):
    try:
        return analyze(request.review)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/batch_analysis")
def batch_analysis():
    try:
        reviews = [analyze(t) for t in SAMPLE_REVIEWS]
        total = len(reviews)
        counts = {k: sum(r["sentiment"] == k.upper() for r in reviews)
                  for k in ("positive", "negative", "neutral")}
        stats = {**counts, **{f"{k}_pct": round(v * 100 / total, 1) for k, v in counts.items()}}
        return {"total_reviews": total, "summary_stats": stats, "reviews": reviews}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "ok"}