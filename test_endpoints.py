import httpx
import asyncio

BASE_URL = "https://today-api-7f3i.onrender.com"

endpoints = [
    "/",
    "/fixtures?date=2025-06-15",
    "/live",
    "/fixtures/events/215662",
    "/fixtures/lineups/215662",
    "/fixtures/statistics/215662",
    "/fixtures/headtohead/33/34",
    "/odds/215662",
    "/predictions/215662",
    "/odds/live",
    "/odds/live/bets",
    "/standings/39",
    "/leagues",
    "/leagues/seasons",
    "/teams",
    "/teams/statistics/33/39",
    "/teams/countries",
    "/players?team_id=33&season=2024",
    "/players/statistics/276/39",
    "/players/topscorers/39",
    "/players/topassists/39",
    "/players/topyellowcards/39",
    "/players/topredcards/39",
    "/players/squads/33/2024",
    "/injuries/39",
    "/injuries?ids=215662,215663",
    "/sidelined?players=276&coachs=34",
    "/transfers/276",
    "/coachs?team_id=33",
    "/trophies?players=276",
]


async def test_endpoint(client, url):
    try:
        response = await client.get(f"{BASE_URL}{url}", timeout=10)
        status = response.status_code
        if status == 200:
            print(f"✅ {url} OK")
        else:
            print(f"⚠️ {url} returned {status}")
    except Exception as e:
        print(f"❌ {url} failed → {e}")


async def main():
    async with httpx.AsyncClient() as client:
        await asyncio.gather(*(test_endpoint(client, url) for url in endpoints))


if __name__ == "__main__":
    asyncio.run(main())
