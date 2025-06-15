
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

# Caches
fixture_cache = TTLCache(maxsize=1000, ttl=300)
predictions_cache = TTLCache(maxsize=1000, ttl=3600)
odds_cache = TTLCache(maxsize=1000, ttl=3600)
general_cache = TTLCache(maxsize=1000, ttl=86400)
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
            if ttl_cache and cache_key:
                async with cache_lock:
                    ttl_cache[cache_key] = data
            return data
    except Exception:
        return {"response": []}

async def get_predictions_cached(fixture_id: int):
    return await fetch("predictions", {"fixture": fixture_id}, predictions_cache, f"pred_{fixture_id}")

async def get_odds_cached(fixture_id: int):
    return await fetch("odds", {"fixture": fixture_id}, odds_cache, f"odds_{fixture_id}")

async def get_fixtures_by_date(date: str):
    cache_key = f"fixtures_{date}"
    data = await fetch("fixtures", {"date": date, "timezone": "Europe/Belgrade"}, fixture_cache, cache_key)
    enriched = []
    for fx in data.get("response", []):
        try:
            fixture = fx.get("fixture", {})
            fid = fixture.get("id")
            timestamp = fixture.get("timestamp")
            if not fid or not timestamp:
                continue

            team_home_logo = fx.get("teams", {}).get("home", {}).get("logo", "")
            team_away_logo = fx.get("teams", {}).get("away", {}).get("logo", "")
            league_logo = fx.get("league", {}).get("logo", "")
            country_flag = fx.get("league", {}).get("flag", "")

            if not all([team_home_logo, team_away_logo, league_logo, country_flag]):
                continue

            pred = await get_predictions_cached(fid)
            odds = await get_odds_cached(fid)
            fx["predictions"] = pred.get("response", [])
            fx["odds"] = odds.get("response", [])

            enriched.append(fx)
        except Exception:
            continue
    return {"response": enriched}
