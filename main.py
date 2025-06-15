from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, timedelta
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

@app.get("/meta/debug-fixtures")
async def debug_fixtures(date: str):
    return await get_fixtures_by_date(date)

@app.get("/fixtures")
async def fixtures(date: str):
    return await get_fixtures_by_date(date)

@app.get("/fixtures/today")
async def fixtures_today():
    return await get_fixtures_by_date(date.today().isoformat())

@app.get("/fixtures/yesterday")
async def fixtures_yesterday():
    return await get_fixtures_by_date((date.today() - timedelta(days=1)).isoformat())

@app.get("/fixtures/tomorrow")
async def fixtures_tomorrow():
    return await get_fixtures_by_date((date.today() + timedelta(days=1)).isoformat())
