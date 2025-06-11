from fastapi import FastAPI
from api_football import (
    get_fixtures_today, get_standings, get_live_fixtures,
    get_odds, get_topscorers, get_injuries, get_headtohead
)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Today API is live"}

@app.get("/fixtures/today")
async def fixtures_today():
    return await get_fixtures_today()

@app.get("/standings/{league_id}")
async def standings(league_id: int):
    return await get_standings(league_id)

@app.get("/live")
async def live():
    return await get_live_fixtures()

@app.get("/odds/{fixture_id}")
async def odds(fixture_id: int):
    return await get_odds(fixture_id)

@app.get("/players/topscorers/{league_id}")
async def players_topscorers(league_id: int):
    return await get_topscorers(league_id)

@app.get("/injuries/{league_id}")
async def injuries(league_id: int):
    return await get_injuries(league_id)

@app.get("/headtohead/{team1_id}/{team2_id}")
async def headtohead(team1_id: int, team2_id: int):
    return await get_headtohead(team1_id, team2_id)
