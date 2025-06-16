
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

# Fixtures with enrichment and filtering (safe version)
async def get_fixtures_by_date(date: str):
    try:
        cache_key = f"fixtures_enriched_{date}"
        async with cache_lock:
            if cache_key in fixture_cache:
                return fixture_cache[cache_key]

        raw = await fetch("fixtures", {"date": date, "timezone": "Europe/Belgrade"}, None, None)
        if not raw or "response" not in raw:
            return {"response": []}

        enriched = []

        for fx in raw["response"]:
            fixture = fx.get("fixture", {})
            teams = fx.get("teams", {})
            league = fx.get("league", {})

            fid = fixture.get("id")
            if not fid:
                continue

            # Safe fetch predictions and odds
            try:
                pred = await get_predictions_cached(fid)
                odds = await get_odds_cached(fid)
            except Exception:
                pred = {"response": []}
                odds = {"response": []}

            fx["predictions"] = pred.get("response", [])
            fx["odds"] = odds.get("response", [])

            # Logos check
            if (
                league.get("logo") and
                teams.get("home", {}).get("logo") and
                teams.get("away", {}).get("logo")
            ):
                enriched.append(fx)

        result = {"response": enriched}
        async with cache_lock:
            fixture_cache[cache_key] = result
        return result

    except Exception as e:
        return {"response": [], "error": str(e)}


# Test funkcija bez filtriranja
async def get_raw_fixtures(date: str):
    return await fetch("fixtures", {"date": date, "timezone": "Europe/Belgrade"}, None, None)
        
async def get_live_fixtures():
    return await fetch("fixtures", {"live": "all", "timezone": "Europe/Belgrade"}, fixture_cache, "live_fixtures")

async def get_events(fixture_id: int):
    return await fetch(f"fixtures/events", {"fixture": fixture_id}, general_cache, f"events_{fixture_id}")

async def get_lineups(fixture_id: int):
    return await fetch(f"fixtures/lineups", {"fixture": fixture_id}, general_cache, f"lineups_{fixture_id}")

async def get_fixture_statistics(fixture_id: int):
    return await fetch(f"fixtures/statistics", {"fixture": fixture_id}, general_cache, f"statistics_{fixture_id}")

async def get_headtohead(team1_id: int, team2_id: int):
    return await fetch("fixtures/headtohead", {"h2h": f"{team1_id}-{team2_id}"}, general_cache, f"h2h_{team1_id}_{team2_id}")

# Single fixture enrichment
async def get_predictions_cached(fixture_id: int):
    return await fetch("predictions", {"fixture": fixture_id}, predictions_cache, f"pred_{fixture_id}")

async def get_odds_cached(fixture_id: int):
    return await fetch("odds", {"fixture": fixture_id}, odds_cache, f"odds_{fixture_id}")

async def get_live_odds():
    return await fetch("odds/live", {}, odds_cache, "live_odds")

async def get_live_odds_bets():
    return await fetch("odds/live/bets", {}, odds_cache, "live_odds_bets")

# Leagues & Standings
async def get_leagues():
    return await fetch("leagues", {}, general_cache, "leagues")

async def get_leagues_seasons():
    return await fetch("leagues/seasons", {}, general_cache, "seasons")

async def get_standings(league_id: int):
    return await fetch("standings", {"league": league_id, "season": date.today().year}, general_cache, f"standings_{league_id}")

# Teams
async def get_teams(country=None, league_id=None, season=None):
    params = {}
    if country: params["country"] = country
    if league_id: params["league"] = league_id
    if season: params["season"] = season
    return await fetch("teams", params, general_cache, f"teams_{country}_{league_id}_{season}")

async def get_team_statistics(team_id: int, league_id: int):
    return await fetch("teams/statistics", {"team": team_id, "league": league_id, "season": date.today().year}, general_cache, f"team_stats_{team_id}_{league_id}")

async def get_teams_countries():
    return await fetch("teams/countries", {}, general_cache, "team_countries")

# Players
async def get_players(team_id: int, season: int):
    return await fetch("players", {"team": team_id, "season": season}, general_cache, f"players_{team_id}_{season}")

async def get_player_statistics(player_id: int, league_id: int):
    return await fetch("players/statistics", {"player": player_id, "league": league_id, "season": date.today().year}, general_cache, f"player_stats_{player_id}_{league_id}")

async def get_topscorers(league_id: int):
    return await fetch("players/topscorers", {"league": league_id, "season": date.today().year}, general_cache, f"topscorers_{league_id}")

async def get_topassists(league_id: int):
    return await fetch("players/topassists", {"league": league_id, "season": date.today().year}, general_cache, f"topassists_{league_id}")

async def get_topyellowcards(league_id: int):
    return await fetch("players/topyellowcards", {"league": league_id, "season": date.today().year}, general_cache, f"topyellow_{league_id}")

async def get_topredcards(league_id: int):
    return await fetch("players/topredcards", {"league": league_id, "season": date.today().year}, general_cache, f"topred_{league_id}")

async def get_squad(team_id: int, season: int):
    return await fetch("players/squads", {"team": team_id, "season": season}, general_cache, f"squad_{team_id}_{season}")

# Injuries & Transfers
async def get_injuries(league_id: int = None, ids: str = None):
    params = {}
    if league_id: params["league"] = league_id
    if ids: params["fixture"] = ids
    return await fetch("injuries", params, general_cache, f"injuries_{league_id}_{ids}")

async def get_sidelined(players=None, coachs=None):
    params = {}
    if players: params["player"] = players
    if coachs: params["coach"] = coachs
    return await fetch("sidelined", params, general_cache, f"sidelined_{players}_{coachs}")

# Transfers & Coachs & Trophies
async def get_transfers(player_id: int):
    return await fetch("transfers", {"player": player_id}, general_cache, f"transfers_{player_id}")

async def get_coachs(team_id=None, search=None):
    params = {}
    if team_id: params["team"] = team_id
    if search: params["search"] = search
    return await fetch("coachs", params, general_cache, f"coachs_{team_id}_{search}")

async def get_trophies(players=None, coachs=None):
    params = {}
    if players: params["player"] = players
    if coachs: params["coach"] = coachs
    return await fetch("trophies", params, general_cache, f"trophies_{players}_{coachs}")

async def fetch_odds_general(fixture=None, league=None, season=None, date=None):
    params = {}
    if fixture: params["fixture"] = fixture
    if league: params["league"] = league
    if season: params["season"] = season
    if date: params["date"] = date
    return await fetch("odds", params, odds_cache, f"odds_{fixture}_{league}_{season}_{date}")

