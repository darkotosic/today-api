import asyncio
from datetime import date, timedelta

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse, PlainTextResponse

from api_football import (
    get_fixtures_by_date,
    get_raw_fixtures,
    get_live_fixtures,
    get_events,
    get_lineups,
    get_fixture_statistics,
    get_headtohead,
    get_odds_cached,
    get_predictions_cached,
    get_live_odds,
    get_live_odds_bets,
    fetch_odds_general,
    get_leagues,
    get_leagues_seasons,
    get_standings,
    get_teams,
    get_team_statistics,
    get_teams_countries,
    get_players,
    get_player_statistics,
    get_topscorers,
    get_topassists,
    get_topyellowcards,
    get_topredcards,
    get_squad,
    get_injuries,
    get_sidelined,
    get_transfers,
    get_coachs,
    get_trophies,
    get_predictions_by_date,
    get_odds_by_date,
    get_comparison_by_date
)

app = FastAPI(default_response_class=ORJSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return ORJSONResponse({"error": "Internal server error"}, status_code=500)


@app.get("/")
async def root():
    return {"message": "Today API is live"}


# ─── Fixtures ─────────────────────────────────────────────────────────────────

@app.get("/fixtures")
async def fixtures(date: str):
    return await get_fixtures_by_date(date)


@app.get("/fixtures/today")
async def fixtures_today():
    return await get_fixtures_by_date(date.today().isoformat())


@app.get("/fixtures/yesterday")
async def fixtures_yesterday():
    d = (date.today() - timedelta(days=1)).isoformat()
    return await get_fixtures_by_date(d)


@app.get("/fixtures/tomorrow")
async def fixtures_tomorrow():
    d = (date.today() + timedelta(days=1)).isoformat()
    return await get_fixtures_by_date(d)


@app.get("/fixtures/full-today")
async def full_today():
    today_str = date.today().isoformat()
    raw = await get_raw_fixtures(today_str)
    fixtures_list = raw.get("response", [])
    tasks = [
        asyncio.gather(
            get_predictions_cached(fx["fixture"]["id"]),
            get_odds_cached(fx["fixture"]["id"])
        )
        for fx in fixtures_list
    ]
    results = []
    if tasks:
        preds_odds = await asyncio.gather(*tasks)
        for fx, (pred, odds) in zip(fixtures_list, preds_odds):
            fx["predictions"] = pred.get("response", [])
            fx["odds"] = odds.get("response", [])
            results.append(fx)
    return {"response": results}


@app.get("/fixtures/full-details")
async def full_fixture_details(date: str):
    raw = await get_raw_fixtures(date)
    fixtures_list = raw.get("response", [])
    tasks = []
    for fx in fixtures_list:
        fid = fx["fixture"]["id"]
        home_id = fx["teams"]["home"]["id"]
        away_id = fx["teams"]["away"]["id"]
        tasks.append(asyncio.gather(
            get_predictions_cached(fid),
            get_odds_cached(fid),
            get_events(fid),
            get_lineups(fid),
            get_fixture_statistics(fid),
            get_headtohead(home_id, away_id),
        ))
    results = []
    if tasks:
        all_data = await asyncio.gather(*tasks)
        for fx, data in zip(fixtures_list, all_data):
            pred, odds, events, lineups, stats, h2h = data
            fx["predictions"] = pred.get("response", [])
            fx["odds"] = odds.get("response", [])
            fx["events"] = events.get("response", [])
            fx["lineups"] = lineups.get("response", [])
            fx["statistics"] = stats.get("response", [])
            fx["h2h"] = h2h.get("response", [])
            results.append(fx)
    return {"response": results}


@app.get("/live")
async def live():
    return await get_live_fixtures()


# ─── Odds & Predictions ────────────────────────────────────────────────────────

@app.get("/odds/{fixture_id}")
async def odds(fixture_id: int):
    return await get_odds_cached(fixture_id)


@app.get("/predictions/{fixture_id}")
async def predictions(fixture_id: int):
    return await get_predictions_cached(fixture_id)


@app.get("/odds/live")
async def odds_live():
    return await get_live_odds()


@app.get("/odds/live/bets")
async def odds_live_bets():
    return await get_live_odds_bets()


@app.get("/odds")
async def odds_all(
    fixture: int = None,
    league: int = None,
    season: int = None,
    date: str = None
):
    return await fetch_odds_general(fixture, league, season, date)


# ─── Leagues & Standings ───────────────────────────────────────────────────────

@app.get("/leagues")
async def leagues():
    return await get_leagues()


@app.get("/leagues/seasons")
async def leagues_seasons():
    return await get_leagues_seasons()


@app.get("/standings/{league_id}")
async def standings(league_id: int):
    return await get_standings(league_id)


# ─── Teams ─────────────────────────────────────────────────────────────────────

@app.get("/teams")
async def teams(country: str = None, league_id: int = None, season: int = None):
    return await get_teams(country, league_id, season)


@app.get("/teams/statistics/{team_id}/{league_id}")
async def team_statistics(team_id: int, league_id: int):
    return await get_team_statistics(team_id, league_id)


@app.get("/teams/countries")
async def teams_countries():
    return await get_teams_countries()


# ─── Players ───────────────────────────────────────────────────────────────────

@app.get("/players")
async def players(team_id: int, season: int):
    return await get_players(team_id, season)


@app.get("/players/statistics/{player_id}/{league_id}")
async def player_statistics(player_id: int, league_id: int):
    return await get_player_statistics(player_id, league_id)


@app.get("/players/topscorers/{league_id}")
async def players_topscorers(league_id: int):
    return await get_topscorers(league_id)


@app.get("/players/topassists/{league_id}")
async def players_topassists(league_id: int):
    return await get_topassists(league_id)


@app.get("/players/topyellowcards/{league_id}")
async def players_topyellowcards(league_id: int):
    return await get_topyellowcards(league_id)


@app.get("/players/topredcards/{league_id}")
async def players_topredcards(league_id: int):
    return await get_topredcards(league_id)


@app.get("/players/squads/{team_id}/{season}")
async def players_squads(team_id: int, season: int):
    return await get_squad(team_id, season)


# ─── Injuries & Transfers ──────────────────────────────────────────────────────

@app.get("/injuries")
async def injuries(league_id: int = None, ids: str = None):
    return await get_injuries(league_id, ids)


@app.get("/sidelined")
async def sidelined(players: str = None, coaches: str = None):
    return await get_sidelined(players, coaches)


# ─── Transfers, Coaches & Trophies ─────────────────────────────────────────────

@app.get("/transfers/{player_id}")
async def transfers(player_id: int):
    return await get_transfers(player_id)


@app.get("/coachs")
async def coachs(team_id: int = None, search: str = None):
    return await get_coachs(team_id, search)


@app.get("/trophies")
async def trophies(players: str = None, coaches: str = None):
    return await get_trophies(players, coaches)


# ─── Test & Bulk Endpoints ─────────────────────────────────────────────────────

@app.get("/test")
async def test_raw(date: str):
    return await get_raw_fixtures(date)


@app.get("/teams/statistics/all")
async def all_team_stats():
    leagues_data = await get_leagues()
    leagues = leagues_data.get("response", [])
    teams_tasks = [
        get_teams(league_id=lg["league"]["id"], season=lg["seasons"][-1]["year"])
        for lg in leagues
    ]
    teams_results = await asyncio.gather(*teams_tasks)

    stats_tasks = []
    for lg, team_list in zip(leagues, teams_results):
        lid = lg["league"]["id"]
        for t in team_list.get("response", []):
            stats_tasks.append(get_team_statistics(t["team"]["id"], lid))
    stats_results = await asyncio.gather(*stats_tasks)

    response = []
    idx = 0
    for lg, team_list in zip(leagues, teams_results):
        lid = lg["league"]["id"]
        for t in team_list.get("response", []):
            response.append({
                "team_id": t["team"]["id"],
                "league_id": lid,
                "stats": stats_results[idx].get("response", {})
            })
            idx += 1
    return {"response": response}


@app.get("/standings/all")
async def all_standings():
    leagues_data = await get_leagues()
    leagues = leagues_data.get("response", [])
    standings_tasks = [get_standings(lg["league"]["id"]) for lg in leagues]
    standings_results = await asyncio.gather(*standings_tasks)

    response = [
        {"league_id": lg["league"]["id"], "standings": res.get("response", [])}
        for lg, res in zip(leagues, standings_results)
    ]
    return {"response": response}

@app.get("/predictions")
async def predictions(date: str):
    return await get_predictions_by_date(date)

@app.get("/odds")
async def odds(date: str):
    return await get_odds_by_date(date)

@app.get("/comparison")
async def comparison(date: str):
    return await get_comparison_by_date(date)

# ─── DODAJ OVO NA DNO: /ping ruta ──────────────────────────────

@app.get("/ping", response_class=PlainTextResponse)
async def ping():
    return "pong"
