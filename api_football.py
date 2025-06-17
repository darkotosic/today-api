import os
import asyncio
from datetime import date
from typing import Any, Dict, Optional

import httpx
from cachetools import TTLCache
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_KEY}

# —――――――――――――――――――――――――――――――――
# Global HTTP client (reused for all requests)
# HTTP/2 enabled for multiplexing
_client = httpx.AsyncClient(
    base_url=BASE_URL,
    headers=HEADERS,
    timeout=5.0,
    http2=True
)

# —――――――――――――――――――――――――――――――――
# Caches with asyncio lock to avoid race conditions
fixture_cache     = TTLCache(maxsize=1000, ttl=300)
predictions_cache = TTLCache(maxsize=1000, ttl=3600)
odds_cache        = TTLCache(maxsize=1000, ttl=3600)
general_cache     = TTLCache(maxsize=1000, ttl=86400)
_cache_lock       = asyncio.Lock()


async def fetch(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    cache: Optional[TTLCache] = None,
    cache_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Core fetcher that reuses a single HTTPX client,
    optionally caches responses in an async-safe TTLCache.
    """
    # Check cache
    if cache is not None and cache_key is not None:
        async with _cache_lock:
            if cache_key in cache:
                return cache[cache_key]

    try:
        resp = await _client.get(endpoint, params=params)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        # On any error (timeout, HTTP error, JSON decode, etc.), return empty response
        data = {"response": []}

    # Store in cache
    if cache is not None and cache_key is not None:
        async with _cache_lock:
            cache[cache_key] = data

    return data


# —――――――――――――――――――――――――――――――――
# Fixtures

async def get_raw_fixtures(date_str: str) -> Dict[str, Any]:
    return await fetch(
        "fixtures",
        params={"date": date_str, "timezone": "Europe/Belgrade"}
    )

async def get_live_fixtures() -> Dict[str, Any]:
    return await fetch(
        "fixtures",
        params={"live": "all", "timezone": "Europe/Belgrade"},
        cache=fixture_cache,
        cache_key="live_fixtures"
    )

async def get_fixtures_by_date(date_str: str) -> Dict[str, Any]:
    cache_key = f"fixtures_enriched_{date_str}"
    async with _cache_lock:
        if cache_key in fixture_cache:
            return fixture_cache[cache_key]

    raw = await fetch("fixtures", {"date": date_str, "timezone": "Europe/Belgrade"})
    resp = raw.get("response") or []
    enriched = []

    for fx in resp:
        fixture = fx.get("fixture", {})
        league  = fx.get("league", {})
        teams   = fx.get("teams", {})
        fid     = fixture.get("id")
        if not fid:
            continue

        # Parallel fetch of predictions and odds
        pred_task = get_predictions_cached(fid)
        odds_task = get_odds_cached(fid)
        pred, odds = await asyncio.gather(pred_task, odds_task)

        fx["predictions"] = pred.get("response", [])
        fx["odds"]        = odds.get("response", [])

        # Only include if logos exist
        if league.get("logo") and teams.get("home", {}).get("logo") and teams.get("away", {}).get("logo"):
            enriched.append(fx)

    result = {"response": enriched}
    async with _cache_lock:
        fixture_cache[cache_key] = result
    return result


# —――――――――――――――――――――――――――――――――
# Events, Lineups, Stats, H2H

async def get_events(fixture_id: int) -> Dict[str, Any]:
    return await fetch(
        "fixtures/events",
        params={"fixture": fixture_id},
        cache=general_cache,
        cache_key=f"events_{fixture_id}"
    )

async def get_lineups(fixture_id: int) -> Dict[str, Any]:
    return await fetch(
        "fixtures/lineups",
        params={"fixture": fixture_id},
        cache=general_cache,
        cache_key=f"lineups_{fixture_id}"
    )

async def get_fixture_statistics(fixture_id: int) -> Dict[str, Any]:
    return await fetch(
        "fixtures/statistics",
        params={"fixture": fixture_id},
        cache=general_cache,
        cache_key=f"statistics_{fixture_id}"
    )

async def get_headtohead(team1_id: int, team2_id: int) -> Dict[str, Any]:
    return await fetch(
        "fixtures/headtohead",
        params={"h2h": f"{team1_id}-{team2_id}"},
        cache=general_cache,
        cache_key=f"h2h_{team1_id}_{team2_id}"
    )


# —――――――――――――――――――――――――――――――――
# Predictions & Odds

async def get_predictions_cached(fixture_id: int) -> Dict[str, Any]:
    return await fetch(
        "predictions",
        params={"fixture": fixture_id},
        cache=predictions_cache,
        cache_key=f"pred_{fixture_id}"
    )

async def get_odds_cached(fixture_id: int) -> Dict[str, Any]:
    return await fetch(
        "odds",
        params={"fixture": fixture_id},
        cache=odds_cache,
        cache_key=f"odds_{fixture_id}"
    )

async def get_live_odds() -> Dict[str, Any]:
    return await fetch(
        "odds/live",
        cache=odds_cache,
        cache_key="live_odds"
    )

async def get_live_odds_bets() -> Dict[str, Any]:
    return await fetch(
        "odds/live/bets",
        cache=odds_cache,
        cache_key="live_odds_bets"
    )


# —――――――――――――――――――――――――――――――――
# Leagues & Standings

async def get_leagues() -> Dict[str, Any]:
    return await fetch("leagues", cache=general_cache, cache_key="leagues")

async def get_leagues_seasons() -> Dict[str, Any]:
    return await fetch("leagues/seasons", cache=general_cache, cache_key="seasons")

async def get_standings(league_id: int) -> Dict[str, Any]:
    return await fetch(
        "standings",
        params={"league": league_id, "season": date.today().year},
        cache=general_cache,
        cache_key=f"standings_{league_id}"
    )


# —――――――――――――――――――――――――――――――――
# Teams & Players

async def get_teams(country: Optional[str] = None,
                    league_id: Optional[int] = None,
                    season: Optional[int] = None) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if country:    params["country"] = country
    if league_id:  params["league"]  = league_id
    if season:     params["season"]  = season
    key = f"teams_{country}_{league_id}_{season}"
    return await fetch("teams", params=params, cache=general_cache, cache_key=key)

async def get_team_statistics(team_id: int, league_id: int) -> Dict[str, Any]:
    return await fetch(
        "teams/statistics",
        params={"team": team_id, "league": league_id, "season": date.today().year},
        cache=general_cache,
        cache_key=f"team_stats_{team_id}_{league_id}"
    )

async def get_teams_countries() -> Dict[str, Any]:
    return await fetch("teams/countries", cache=general_cache, cache_key="team_countries")

async def get_players(team_id: int, season: int) -> Dict[str, Any]:
    return await fetch(
        "players",
        params={"team": team_id, "season": season},
        cache=general_cache,
        cache_key=f"players_{team_id}_{season}"
    )

async def get_player_statistics(player_id: int, league_id: int) -> Dict[str, Any]:
    return await fetch(
        "players/statistics",
        params={"player": player_id, "league": league_id, "season": date.today().year},
        cache=general_cache,
        cache_key=f"player_stats_{player_id}_{league_id}"
    )

async def get_topscorers(league_id: int) -> Dict[str, Any]:
    return await fetch(
        "players/topscorers",
        params={"league": league_id, "season": date.today().year},
        cache=general_cache,
        cache_key=f"topscorers_{league_id}"
    )

async def get_topassists(league_id: int) -> Dict[str, Any]:
    return await fetch(
        "players/topassists",
        params={"league": league_id, "season": date.today().year},
        cache=general_cache,
        cache_key=f"topassists_{league_id}"
    )

async def get_topyellowcards(league_id: int) -> Dict[str, Any]:
    return await fetch(
        "players/topyellowcards",
        params={"league": league_id, "season": date.today().year},
        cache=general_cache,
        cache_key=f"topyellow_{league_id}"
    )

async def get_topredcards(league_id: int) -> Dict[str, Any]:
    return await fetch(
        "players/topredcards",
        params={"league": league_id, "season": date.today().year},
        cache=general_cache,
        cache_key=f"topred_{league_id}"
    )

async def get_squad(team_id: int, season: int) -> Dict[str, Any]:
    return await fetch(
        "players/squads",
        params={"team": team_id, "season": season},
        cache=general_cache,
        cache_key=f"squad_{team_id}_{season}"
    )


# —――――――――――――――――――――――――――――――――
# Injuries, Transfers, Coaches, Trophies

async def get_injuries(league_id: Optional[int] = None,
                       ids: Optional[str] = None) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if league_id: params["league"] = league_id
    if ids:       params["fixture"] = ids
    key = f"injuries_{league_id}_{ids}"
    return await fetch("injuries", params=params, cache=general_cache, cache_key=key)

async def get_sidelined(players: Optional[str] = None,
                        coaches: Optional[str] = None) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if players: params["player"] = players
    if coaches: params["coach"]  = coaches
    key = f"sidelined_{players}_{coaches}"
    return await fetch("sidelined", params=params, cache=general_cache, cache_key=key)

async def get_transfers(player_id: int) -> Dict[str, Any]:
    return await fetch(
        "transfers",
        params={"player": player_id},
        cache=general_cache,
        cache_key=f"transfers_{player_id}"
    )

async def get_coaches(team_id: Optional[int] = None,
                      search: Optional[str] = None) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if team_id: params["team"]   = team_id
    if search:  params["search"] = search
    key = f"coaches_{team_id}_{search}"
    return await fetch("coachs", params=params, cache=general_cache, cache_key=key)

async def get_trophies(players: Optional[str] = None,
                       coaches: Optional[str] = None) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if players: params["player"] = players
    if coaches: params["coach"]  = coaches
    key = f"trophies_{players}_{coaches}"
    return await fetch("trophies", params=params, cache=general_cache, cache_key=key)
