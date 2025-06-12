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

async def get_odds(fixture_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/odds",
            params={"fixture": fixture_id},
            headers=headers
        )
        return response.json()

async def get_topscorers(league_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/players/topscorers",
            params={"league": league_id, "season": "2024"},
            headers=headers
        )
        return response.json()

async def get_injuries(league_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/injuries",
            params={"league": league_id, "season": "2024"},
            headers=headers
        )
        return response.json()

async def get_headtohead(team1_id: int, team2_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/fixtures/headtohead",
            params={"h2h": f"{team1_id}-{team2_id}"},
            headers=headers
        )
        return response.json()

async def get_events(fixture_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/fixtures/events",
            params={"fixture": fixture_id},
            headers=headers
        )
        return response.json()

async def get_lineups(fixture_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/fixtures/lineups",
            params={"fixture": fixture_id},
            headers=headers
        )
        return response.json()

async def get_fixture_statistics(fixture_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/fixtures/statistics",
            params={"fixture": fixture_id},
            headers=headers
        )
        return response.json()

async def get_team_statistics(team_id: int, league_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/teams/statistics",
            params={"team": team_id, "league": league_id, "season": "2024"},
            headers=headers
        )
        return response.json()

async def get_player_statistics(player_id: int, league_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/players",
            params={"id": player_id, "league": league_id, "season": "2024"},
            headers=headers
        )
        return response.json()

async def get_predictions(fixture_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/predictions",
            params={"fixture": fixture_id},
            headers=headers
        )
        return response.json()
    
async def get_leagues():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/leagues",
            headers=headers
        )
        return response.json()


async def get_fixtures_by_date(date: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/fixtures",
            params={"date": date},
            headers=headers
        )
        return response.json()
    

async def get_players(team_id: int, season: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/players",
            params={"team": team_id, "season": season},
            headers=headers
        )
        return response.json()

async def get_teams(country: str = None, league_id: int = None, season: int = None):
    async with httpx.AsyncClient() as client:
        params = {}
        if country:
            params["country"] = country
        if league_id:
            params["league"] = league_id
        if season:
            params["season"] = season

        response = await client.get(
            f"{BASE_URL}/teams",
            params=params,
            headers=headers
        )
        return response.json()

async def get_leagues_seasons():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/leagues/seasons",
            headers=headers
        )
        return response.json()

async def get_transfers(player_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/transfers",
            params={"player": player_id},
            headers=headers
        )
        return response.json()

async def get_coachs(team_id: int = None, search: str = None):
    async with httpx.AsyncClient() as client:
        params = {}
        if team_id:
            params["team"] = team_id
        if search:
            params["search"] = search

        response = await client.get(
            f"{BASE_URL}/coachs",
            params=params,
            headers=headers
        )
        return response.json()
