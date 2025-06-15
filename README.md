# ⚽ Today API – Multipurpose Football Backend

A powerful backend built on **FastAPI** that integrates **API-FOOTBALL V3**, built to serve:

✅ Web apps  
✅ Android apps  
✅ Telegram bots  
✅ Admin dashboards  
✅ Internal prediction tools  

---


---

## 📡 Endpoints Overview

### 🗓 Fixtures
- `GET /fixtures?date=YYYY-MM-DD` – Matches for selected date
- `GET /fixtures/events/{fixture_id}`
- `GET /fixtures/lineups/{fixture_id}`
- `GET /fixtures/statistics/{fixture_id}`
- `GET /fixtures/headtohead/{team1_id}/{team2_id}`
- `GET /live`

### 📊 Odds & Predictions
- `GET /odds/{fixture_id}`
- `GET /predictions/{fixture_id}`
- `GET /odds/live`
- `GET /odds/live/bets`

### 🏆 Leagues
- `GET /leagues`
- `GET /leagues/seasons`
- `GET /standings/{league_id}`

### 👥 Teams
- `GET /teams?country=&league_id=&season=`
- `GET /teams/statistics/{team_id}/{league_id}`
- `GET /teams/countries`

### 🧍‍♂️ Players
- `GET /players?team_id=&season=`
- `GET /players/statistics/{player_id}/{league_id}`
- `GET /players/topscorers/{league_id}`
- `GET /players/topassists/{league_id}`
- `GET /players/topyellowcards/{league_id}`
- `GET /players/topredcards/{league_id}`
- `GET /players/squads/{team_id}/{season}`

### 🩼 Injuries & Sidelined
- `GET /injuries/{league_id}`
- `GET /injuries?ids=...`
- `GET /sidelined?players=...&coachs=...`

### 🔁 Transfers & Coachs
- `GET /transfers/{player_id}`
- `GET /coachs?team_id=&search=...`

### 🏅 Trophies
- `GET /trophies?players=...&coachs=...`

---

## ⚙️ Tech Stack
- FastAPI
- httpx (async client)
- cachetools (TTLCache)
- python-dotenv
- Deployed on Render.com

---

## 🔐 .env setup
API_FOOTBALL_KEY=your_api_key_here
BASE_URL=https://v3.football.api-sports.io
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

♻️ Design Philosophy
🔁 Fully multipurpose – reusable across frontend, mobile, bot projects

✅ All endpoints return {"response": [...]} format

🧠 Built-in intelligent caching to reduce API usage

🧩 Easily extendable to new API-FOOTBALL endpoints

---

## 🚀 Local Development

```bash
pip install -r requirements.txt
uvicorn main:app --reload

