# server/djangoapp/restapis.py
import os
import logging
import requests
from urllib.parse import urljoin, quote

from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

# Accept BOTH uppercase and lowercase env vars, prefer uppercase (conventional)
BACKEND_URL = (
    os.getenv("BACKEND_URL")
    or os.getenv("backend_url")
    or "http://localhost:3030"
)
SENTIMENT_URL = (
    os.getenv("SENTIMENT_URL")
    or os.getenv("sentiment_analyzer_url")
    or ""  # empty => disabled/fallback to neutral
)

def _join(base: str, endpoint: str) -> str:
    """Slash-safe join of base + endpoint."""
    if not base:
        raise ValueError("Base URL is empty")
    # ensure base ends with '/', urljoin handles double slashes
    if not base.endswith("/"):
        base = base + "/"
    return urljoin(base, endpoint.lstrip("/"))

def get_request(endpoint: str, **kwargs):
    """
    Wrapper around GET to the Node backend.
    Usage:
      get_request("/fetchDealers")
      get_request("/fetchDealers/California")
      get_request("/fetchReviews/dealer/2")
    """
    url = _join(BACKEND_URL, endpoint)
    try:
        # requests will encode **kwargs into the querystring properly
        resp = requests.get(url, params=kwargs or None, timeout=10)
        resp.raise_for_status()
        print("GET from", resp.url)
        if resp.content:
            return resp.json()
        return None
    except Exception as e:
        print("Network exception occurred", e)
        return None

def analyze_review_sentiments(text: str):
    """
    Optional sentiment analyzer. If SENTIMENT_URL is not set or the service
    fails, return a neutral sentiment to keep the UI flowing.
    """
    if not SENTIMENT_URL:
        return {"sentiment": "neutral", "confidence": 0, "reason": "disabled"}

    try:
        # URL-encode the text segment
        url = _join(SENTIMENT_URL, f"analyze/{quote(text or '')}")
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json() if resp.content else {}
        return {
            "sentiment": data.get("sentiment") or data.get("label") or "neutral",
            "confidence": data.get("confidence", 0),
        }
    except Exception as e:
        logger.warning("Sentiment service failed: %s", e)
        return {"sentiment": "neutral", "confidence": 0, "reason": "fallback"}

def post_review(data_dict: dict):
    url = _join(BACKEND_URL, "/insert_review")
    try:
        resp = requests.post(url, json=data_dict, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print("Network exception occurred", e)
        return None
