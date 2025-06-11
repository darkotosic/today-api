from fastapi import FastAPI
from api_football import get_fixtures_today, get_standings, get_live_fixtures

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
