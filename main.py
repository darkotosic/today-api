from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api_football import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Today API is live"}

# Fixtures & Related
@app.get("/fixtures")
async def fixtures(date: str):
    return await get_fixtures_by_date(date)

@app.get("/live")
async def live():
    return await get_live_fixtures()

@app.get("/fixtures/events/{fixture_id}")
async def events(fixture_id: int):
    return await get_events(fixture_id)

@app.get("/fixtures/lineups/{fixture_id}")
async def lineups(fixture_id: int):
    return await get_lineups(fixture_id)

@app.get("/fixtures/statistics/{fixture_id}")
async def fixture_statistics(fixture_id: int):
    return await get_fixture_statistics(fixture_id)

@app.get("/fixtures/headtohead/{team1_id}/{team2_id}")
async def headtohead(team1_id: int, team2_id: int):
    return await get_headtohead(team1_id, team2_id)

# Odds & Predictions
@app.get("/odds/{fixture_id}")
async def odds(fixture_id: int):
    return await get_odds_cached(fixture_id)

@app.get("/predictions/{fixture_id}")
async def predictions(fixture_id: int):
    return await get_predictions_cached(fixture_id)

# Standings & League Info
@app.get("/standings/{league_id}")
async def standings(league_id: int):
    return await get_standings(league_id)

@app.get("/leagues")
async def leagues():
    return await get_leagues()

@app.get("/leagues/seasons")
async def leagues_seasons():
    return await get_leagues_seasons()

# Teams
@app.get("/teams")
async def teams(country: str = None, league_id: int = None, season: int = None):
    return await get_teams(country, league_id, season)

@app.get("/teams/statistics/{team_id}/{league_id}")
async def team_statistics(team_id: int, league_id: int):
    return await get_team_statistics(team_id, league_id)

@app.get("/teams/countries")
async def teams_countries():
    return await get_teams_countries()

# Players
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
async def players_topyellow(league_id: int):
    return await get_topyellowcards(league_id)

@app.get("/players/topredcards/{league_id}")
async def players_topred(league_id: int):
    return await get_topredcards(league_id)

@app.get("/players/squads/{team_id}/{season}")
async def players_squads(team_id: int, season: int):
    return await get_players_squad(team_id, season)

# Injuries & Sidelined
@app.get("/injuries/{league_id}")
async def injuries(league_id: int):
    return await get_injuries(league_id)

@app.get("/injuries")
async def injuries_by_ids(ids: str):
    return await get_injuries_by_ids(ids)

@app.get("/sidelined")
async def sidelined(players: str = None, coachs: str = None):
    return await get_sidelined(players, coachs)

# Transfers & Coachs
@app.get("/transfers/{player_id}")
async def transfers(player_id: int):
    return await get_transfers(player_id)

@app.get("/coachs")
async def coachs(team_id: int = None, search: str = None):
    return await get_coachs(team_id, search)

# Trophies
@app.get("/trophies")
async def trophies(players: str = None, coachs: str = None):
    return await get_trophies(players, coachs)

# Live Odds
@app.get("/odds/live")
async def odds_live():
    return await get_odds_live()

@app.get("/odds/live/bets")
async def odds_live_bets():
    return await get_odds_live_bets()
