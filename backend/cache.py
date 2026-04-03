import hashlib
import json
import threading
import time

CACHE_TTL = 3600
CACHE_MAX_ITEMS = 1000

_cache = {}
_lock = threading.Lock()


def make_cache_key(question: str, topic_key: str = "") -> str:
    payload = {
        "question": (question or "").strip(),
        "topic_key": (topic_key or "").strip(),
    }
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def cache_get(key):
    with _lock:
        entry = _cache.get(key)
        if not entry:
            return None

        if time.time() - entry["ts"] > CACHE_TTL:
            del _cache[key]
            return None

        return entry["value"]


def cache_set(key, value):
    with _lock:
        if len(_cache) >= CACHE_MAX_ITEMS:
            oldest_key = min(_cache, key=lambda k: _cache[k]["ts"])
            del _cache[oldest_key]

        _cache[key] = {
            "value": value,
            "ts": time.time(),
        }