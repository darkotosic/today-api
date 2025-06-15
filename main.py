from fastapi import FastAPI from fastapi.middleware.cors import CORSMiddleware from datetime import date, timedelta from api_football import *

app = FastAPI()

app.add_middleware( CORSMiddleware, allow_origins=[""], allow_credentials=True, allow_methods=[""], allow_headers=["*"], )

@app.get("/") def root(): return {"message": "Today API is live"}

@app.get("/meta/debug-fixtures") async def debug_fixtures(date: str): return await get_fixtures_by_date(date)

Fixtures & Related

@app.get("/fixtures") async def fixtures(date: str): return await get_fixtures_by_date(date)

@app.get("/fixtures/today") async def fixtures_today(): return await get_fixtures_by_date(date.today().isoformat())

@app.get("/fixtures/yesterday") async def fixtures_yesterday(): return await get_fixtures_by_date((date.today() - timedelta(days=1)).isoformat())

@app.get("/fixtures/tomorrow") async def fixtures_tomorrow(): return await get_fixtures_by_date((date.today() + timedelta(days=1)).isoformat())

@app.get("/live") async def live(): return await get_live_fixtures()

@app.get("/fixtures/events/{fixture_id}") async def events(fixture_id: int): return await get_events(fixture_id)

@app.get("/fixtures/lineups/{fixture_id}") async def lineups(fixture_id: int): return await get_lineups(fixture_id)

@app.get("/fixtures/statistics/{fixture_id}") async def fixture_statistics(fixture_id: int): return await get_fixture_statistics(fixture_id)

@app.get("/fixtures/headtohead/{team1_id}/{team2_id}") async def headtohead(team1_id: int, team2_id: int): return await get_headtohead(team1_id, team2_id)

Odds & Predictions

@app.get("/odds/{fixture_id}") async def odds(fixture_id: int): return await get_odds_cached(fixture_id)

@app.get("/predictions/{fixture_id}") async def predictions(fixture_id: int): return await get_predictions_cached(fixture_id)

@app.get("/odds/batch") async def batch_odds(fixtures: str): ids = fixtures.split(",") results = [] for fid in ids: data = await get_odds_cached(int(fid)) results.append({"fixture_id": fid, "odds": data}) return {"response": results}

@app.get("/predictions/batch") async def batch_predictions(fixtures: str): ids = fixtures.split(",") results = [] for fid in ids: data = await get_predictions_cached(int(fid)) results.append({"fixture_id": fid, "predictions": data}) return {"response": results}

@app.get("/odds/all") async def all_odds(date: str): fixtures_data = await get_fixtures_by_date(date) fixtures = fixtures_data.get("response", []) results = [] for fx in fixtures: fid = fx["fixture"]["id"] odds = await get_odds_cached(fid) results.append({"fixture_id": fid, "odds": odds}) return {"response": results}

@app.get("/predictions/all") async def all_predictions(date: str): fixtures_data = await get_fixtures_by_date(date) fixtures = fixtures_data.get("response", []) results = [] for fx in fixtures: fid = fx["fixture"]["id"] pred = await get_predictions_cached(fid) results.append({"fixture_id": fid, "predictions": pred}) return {"response": results}

@app.get("/odds/live") async def odds_live(): return await get_odds_live()

@app.get("/odds/live/bets") async def odds_live_bets(): return await get_odds_live_bets()

Standings & League Info

@app.get("/standings/{league_id}") async def standings(league_id: int): return await get_standings(league_id)

@app.get("/standings/all") async def all_standings(league_ids: str): ids = league_ids.split(",") results = [] for lid in ids: standings = await get_standings(int(lid)) results.append({"league_id": lid, "data": standings}) return {"response": results}

@app.get("/leagues") async def leagues(): return await get_leagues()

@app.get("/leagues/seasons") async def leagues_seasons(): return await get_leagues_seasons()

Teams

@app.get("/teams") async def teams(country: str = None, league_id: int = None, season: int = None): return await get_teams(country, league_id, season)

@app.get("/teams/all") async def teams_all(league_ids: str, season: int): ids = league_ids.split(",") results = [] for lid in ids: teams = await get_teams(None, int(lid), season) results.append({"league_id": lid, "data": teams}) return {"response": results}

@app.get("/teams/statistics/{team_id}/{league_id}") async def team_statistics(team_id: int, league_id: int): return await get_team_statistics(team_id, league_id)

@app.get("/teams/countries") async def teams_countries(): return await get_teams_countries()

Players

@app.get("/players") async def players(team_id: int, season: int): return await get_players(team_id, season)

@app.get("/players/statistics/{player_id}/{league_id}") async def player_statistics(player_id: int, league_id: int): return await get_player_statistics(player_id, league_id)

@app.get("/players/topscorers/{league_id}") async def players_topscorers(league_id: int): return await get_topscorers(league_id)

@app.get("/players/topassists/{league_id}") async def players_topassists(league_id: int): return await get_topassists(league_id)

@app.get("/players/topyellowcards/{league_id}") async def players_topyellow(league_id: int): return await get_topyellowcards(league_id)

@app.get("/players/topredcards/{league_id}") async def players_topred(league_id: int): return await get_topredcards(league_id)

@app.get("/players/squads/{team_id}/{season}") async def players_squads(team_id: int, season: int): return await get_players_squad(team_id, season)

Injuries & Sidelined

@app.get("/injuries/{league_id}") async def injuries(league_id: int): return await get_injuries(league_id)

@app.get("/injuries") async def injuries_by_ids(ids: str): return await get_injuries_by_ids(ids)

@app.get("/sidelined") async def sidelined(players: str = None, coachs: str = None): return await get_sidelined(players, coachs)

Transfers & Coachs

@app.get("/transfers/{player_id}") async def transfers(player_id: int): return await get_transfers(player_id)

@app.get("/coachs") async def coachs(team_id: int = None, search: str = None): return await get_coachs(team_id, search)

Trophies

@app.get("/trophies") async def trophies(players: str = None, coachs: str = None): return await get_trophies(players, coachs)

