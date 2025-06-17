import os
import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from datetime import date

# importuj app i modele
from main import app  # FastAPI instanca
from models import (
    FixturesResponse,
    LeaguesResponse,
    StandingsResponse,
    TeamsResponse,
    LeagueSeasons,
)

# omogućavamo pytest-asyncio
pytest_plugins = ("pytest_asyncio",)

# svaki test koristi isti AsyncClient
@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

# Tipičan datum za testove
TEST_DATE = os.getenv("TEST_DATE", date.today().isoformat())

# Parametrizovani testovi: (putanja, model za validaciju)
ENDPOINT_TESTS = [
    ("/", dict),  # health check
    (f"/fixtures?date={TEST_DATE}", FixturesResponse),
    ("/fixtures/today", FixturesResponse),
    ("/fixtures/yesterday", FixturesResponse),
    ("/fixtures/tomorrow", FixturesResponse),
    ("/leagues", LeaguesResponse),
    ("/leagues/seasons", LeagueSeasons),
    ("/standings/39", StandingsResponse),
    ("/teams?country=England&league_id=39&season=2025", TeamsResponse),
]

@pytest.mark.asyncio
@pytest.mark.parametrize("path,model", ENDPOINT_TESTS)
async def test_endpoint_returns_valid_response(client: AsyncClient, path: str, model):
    """
    Pokreni GET nad svakim endpoint-om i parsiraj odgovor u odgovarajući Pydantic model.
    """
    r = await client.get(path)
    assert r.status_code == 200, f"{path} vratio {r.status_code}"
    data = r.json()
    # ako je model dict, samo proverimo da je JSON
    if model is dict:
        assert isinstance(data, dict)
    else:
        # pokuša parsiranje u Pydantic model
        model.parse_obj(data)

# test za full-details (kompleksniji, proverava makar jedan fixture)
@pytest.mark.asyncio
async def test_full_details_contains_expected_keys(client: AsyncClient):
    r = await client.get(f"/fixtures/full-details?date={TEST_DATE}")
    assert r.status_code == 200
    data = r.json()
    assert "response" in data and isinstance(data["response"], list)
    if data["response"]:
        fx = data["response"][0]
        # osnovni atributi
        for key in ("fixture", "league", "teams", "predictions", "odds", "events", "lineups", "statistics", "h2h"):
            assert key in fx, f"Missing {key} in full-details response"
