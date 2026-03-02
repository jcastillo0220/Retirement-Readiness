import time
from typing import Optional

CACHE_TTL = 60 * 60  # 1 hour
CACHE_MAX_ITEMS = 1000
_cache = {}

def make_cache_key(prompt: str, topic_key: Optional[str]):
    key = (prompt or "").strip().lower()
    if topic_key:
        key = f"{topic_key}||{key}"
    return key

def cache_get(key: str):
    entry = _cache.get(key)
    if not entry:
        return None
    if time.time() - entry["ts"] > CACHE_TTL:
        del _cache[key]
        return None
    return entry

def cache_set(key: str, value: dict):
    if len(_cache) >= CACHE_MAX_ITEMS:
        oldest_key = min(_cache.items(), key=lambda kv: kv[1]["ts"])[0]
        del _cache[oldest_key]
    value["ts"] = time.time()
    _cache[key] = value