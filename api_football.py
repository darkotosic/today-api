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
    for fx in data.get("response", [])[:20]:
        fid = fx["fixture"]["id"]
        pred = await get_predictions_cached(fid)
        odds = await get_odds_cached(fid)
        fx["predictions"] = pred.get("response", [])
        fx["odds"] = odds.get("response", [])
        try:
            if all([
                fx.get("teams", {}).get("home", {}).get("logo"),
                fx.get("teams", {}).get("away", {}).get("logo"),
                fx.get("league", {}).get("logo"),
                fx.get("league", {}).get("name"),
            ]):
                enriched.append(fx)
        except:
            continue
    return {"response": enriched}

async def get_live_fixtures():
    return await fetch("fixtures", {"live": "all"}, fixture_cache, "live")

# Odds & Predictions
async def get_odds_cached(fixture_id: int):
    return await fetch("odds", {"fixture": fixture_id}, odds_cache, f"odds_{fixture_id}")

async def get_predictions_cached(fixture_id: int):
    return await fetch("predictions", {"fixture": fixture_id}, predictions_cache, f"pred_{fixture_id}")

# Standings
async def get_standings(league_id: int):
    return await fetch("standings", {"league": league_id}, general_cache, f"standings_{league_id}")

# Leagues
async def get_leagues():
    return await fetch("leagues", {}, general_cache, "leagues")

async def get_leagues_seasons():
    return await fetch("leagues/seasons", {}, general_cache, "seasons")

# Teams
async def get_teams(country=None, league_id=None, season=None):
    params = {"country": country, "league": league_id, "season": season}
    return await fetch("teams", params, general_cache, f"teams_{country}_{league_id}_{season}")

async def get_teams_countries():
    return await fetch("teams/countries", {}, general_cache, "teams_countries")

async def get_team_statistics(team_id: int, league_id: int):
    return await fetch("teams/statistics", {"team": team_id, "league": league_id}, general_cache, f"team_stats_{team_id}_{league_id}")

# Players
async def get_players(team_id: int, season: int):
    return await fetch("players", {"team": team_id, "season": season}, general_cache, f"players_{team_id}_{season}")

async def get_player_statistics(player_id: int, league_id: int):
    return await fetch("players", {"id": player_id, "league": league_id}, general_cache, f"player_stats_{player_id}_{league_id}")

async def get_topscorers(league_id: int):
    return await fetch("players/topscorers", {"league": league_id}, general_cache, f"topscorers_{league_id}")

async def get_topassists(league_id: int):
    return await fetch("players/topassists", {"league": league_id}, general_cache, f"topassists_{league_id}")

async def get_topyellowcards(league_id: int):
    return await fetch("players/topyellowcards", {"league": league_id}, general_cache, f"topyellow_{league_id}")

async def get_topredcards(league_id: int):
    return await fetch("players/topredcards", {"league": league_id}, general_cache, f"topred_{league_id}")

async def get_players_squad(team_id: int, season: int):
    return await fetch("players/squads", {"team": team_id, "season": season}, general_cache, f"squad_{team_id}_{season}")

# Fixtures details
async def get_events(fixture_id: int):
    return await fetch("fixtures/events", {"fixture": fixture_id}, fixture_cache, f"events_{fixture_id}")

async def get_lineups(fixture_id: int):
    return await fetch("fixtures/lineups", {"fixture": fixture_id}, fixture_cache, f"lineups_{fixture_id}")

async def get_fixture_statistics(fixture_id: int):
    return await fetch("fixtures/statistics", {"fixture": fixture_id}, fixture_cache, f"fxstats_{fixture_id}")

async def get_headtohead(team1_id: int, team2_id: int):
    return await fetch("fixtures/headtohead", {"h2h": f"{team1_id}-{team2_id}"}, fixture_cache, f"h2h_{team1_id}_{team2_id}")

# Injuries
async def get_injuries(league_id: int):
    return await fetch("injuries", {"league": league_id}, general_cache, f"injuries_{league_id}")

async def get_injuries_by_ids(ids: str):
    return await fetch("injuries", {"ids": ids}, general_cache, f"injuries_ids_{ids}")

# Sidelined & Trophies
async def get_sidelined(players: str = None, coachs: str = None):
    return await fetch("sidelined", {"players": players, "coachs": coachs}, general_cache, f"sidelined_{players}_{coachs}")

async def get_trophies(players: str = None, coachs: str = None):
    return await fetch("trophies", {"players": players, "coachs": coachs}, general_cache, f"trophies_{players}_{coachs}")

# Transfers & Coachs
async def get_transfers(player_id: int):
    return await fetch("transfers", {"player": player_id}, general_cache, f"transfers_{player_id}")

async def get_coachs(team_id: int = None, search: str = None):
    return await fetch("coachs", {"team": team_id, "search": search}, general_cache, f"coachs_{team_id}_{search}")

# Live Odds
async def get_odds_live():
    return await fetch("odds/live", {}, fixture_cache, "odds_live")

async def get_odds_live_bets():
    return await fetch("odds/live/bets", {}, fixture_cache, "odds_live_bets")
