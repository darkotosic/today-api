import os
import httpx
import asyncio
from dotenv import load_dotenv
from cachetools import TTLCache
from datetime import date

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_KEY}

# Global caches
CACHE_TTL_SHORT = 300  # 5 min for live
CACHE_TTL_MEDIUM = 3600  # 1h for standard
CACHE_TTL_LONG = 86400  # 24h for static data

fixture_cache = TTLCache(maxsize=1000, ttl=CACHE_TTL_SHORT)
predictions_cache = TTLCache(maxsize=1000, ttl=CACHE_TTL_MEDIUM)
odds_cache = TTLCache(maxsize=1000, ttl=CACHE_TTL_MEDIUM)
general_cache = TTLCache(maxsize=1000, ttl=CACHE_TTL_LONG)

cache_lock = asyncio.Lock()

async def fetch(endpoint, params=None, ttl_cache=None, cache_key=None, timeout=5.0):
    if ttl_cache and cache_key:
        async with cache_lock:
            if cache_key in ttl_cache:
                return ttl_cache[cache_key]

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(f"{BASE_URL}/{endpoint}", params=params, headers=HEADERS)
            data = response.json()
            if ttl_cache is not None and cache_key:
                async with cache_lock:
                    ttl_cache[cache_key] = data
            return data
    except Exception:
        return {"response": []}

# Fixtures
async def get_fixtures_by_date(date: str):
    cache_key = f"fixtures_{date}"
    data = await fetch("fixtures", {"date": date, "timezone": "Europe/Belgrade"}, fixture_cache, cache_key)
    enriched = []
    for fx in data.get("response", []):
        fid = fx.get("fixture", {}).get("id")
        timestamp = fx.get("fixture", {}).get("timestamp")
        if not fid or not timestamp:
            continue

        pred = await get_predictions_cached(fid)
        odds = await get_odds_cached(fid)
        fx["predictions"] = pred.get("response", [])
        fx["odds"] = odds.get("response", [])

        # filtriraj loše podatke
        team_home_logo = fx.get("teams", {}).get("home", {}).get("logo", "")
        team_away_logo = fx.get("teams", {}).get("away", {}).get("logo", "")
        league_logo = fx.get("league", {}).get("logo", "")
        country_flag = fx.get("league", {}).get("flag", "")

        if all([
            team_home_logo and "0.png" not in team_home_logo,
            team_away_logo and "0.png" not in team_away_logo,
            league_logo,
            country_flag
        ]):
            enriched.append(fx)

    return {"response": enriched}

# Ostale funkcije ostaju nepromenjene...
