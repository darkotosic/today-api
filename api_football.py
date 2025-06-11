import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"

headers = {
    "x-apisports-key": API_KEY
}

async def get_fixtures_today():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/fixtures",
            params={"date": "2025-06-11"},
            headers=headers
        )
        return response.json()

async def get_standings(league_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/standings",
            params={"league": league_id, "season": "2024"},
            headers=headers
        )
        return response.json()

async def get_live_fixtures():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/fixtures",
            params={"live": "all"},
            headers=headers
        )
        return response.json()
