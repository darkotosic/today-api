# Today API - General Purpose Football API Backend

This is a general-purpose backend built on **FastAPI** using the official [API-FOOTBALL V3](https://www.api-football.com/documentation-v3) to power:

✅ Web apps  
✅ Android apps  
✅ Telegram bots  
✅ Internal tools  
✅ Admin dashboards  

---

## 🚀 Base URL


---

## ✅ Available Endpoints

### ⚽ Fixtures

- `GET /fixtures/today` → Today fixtures
- `GET /fixtures?date=YYYY-MM-DD` → Fixtures for given date
- `GET /fixtures/events/{fixture_id}` → Match events
- `GET /fixtures/lineups/{fixture_id}` → Match lineups
- `GET /fixtures/statistics/{fixture_id}` → Match statistics

### 📊 Odds & Predictions

- `GET /odds/{fixture_id}` → Match odds (1X2 etc.)
- `GET /predictions/{fixture_id}` → Match predictions (Winner, Advice, %)

### 🏆 Leagues & Standings

- `GET /leagues` → List of leagues
- `GET /standings/{league_id}` → League standings
- `GET /leagues/seasons` → Available seasons

### 👥 Teams & Players

- `GET /teams` → List of teams (by country, league or season)
- `GET /teams/statistics/{team_id}/{league_id}` → Team statistics
- `GET /players` → Players of a team and season
- `GET /players/statistics/{player_id}/{league_id}` → Player statistics
- `GET /players/topscorers/{league_id}` → Top scorers in league

### 🚑 Injuries & Transfers

- `GET /injuries/{league_id}` → League injuries
- `GET /transfers/{player_id}` → Player transfer history

### ⚔️ Head-to-Head & Live Matches

- `GET /headtohead/{team1_id}/{team2_id}` → H2H results
- `GET /live` → Live matches

### 👨‍🏫 Coachs

- `GET /coachs` → List/search coachs

---

## 💻 Tech Stack

- FastAPI
- httpx (async HTTP client)
- Deployed on Render.com

---

## ⚠️ Notes

- This backend is designed to be reusable across **multiple apps/sites/bots** → no endpoints are removed → we only keep adding more capabilities.
- You can extend it easily with any other API-FOOTBALL V3 endpoints as needed.

---

## 🛠️ How to run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
