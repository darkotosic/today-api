# Today API

Lagana FastAPI aplikacija koja obezbeđuje parsirane i keširane endpoint-e nad [API-Football v3](https://www.api-football.com).

---

## 📚 Sadržaj

- [Instalacija](#-instalacija)  
- [Pokretanje](#-pokretanje)  
- [Endpoint-i](#-endpoint-i)  
- [Testiranje](#-testiranje)  
- [Docker](#-docker)  
- [Deploy na Render](#-deploy-na-render)  
- [Dalji razvoj](#-dalji-razvoj)  

---

## 🚀 Instalacija

1. Kloniraj repo:
   ```bash
   git clone https://github.com/your-org/today-api.git
   cd today-api

2. Kreiraj virtualno okruženje i instaliraj:

python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Kopiraj .env.example u .env i popuni:

API_FOOTBALL_KEY=your_api_key
TODAY_API_URL=https://today-api-7f3i.onrender.com

🏃‍♂️ Pokretanje lokalno
uvicorn main:app --host 0.0.0.0 --port 10000 --workers 4
Sada u browseru ili Postman-u:
GET http://localhost:10000/

🔗 Endpoint-i
Za detalje, pogledaj OpenAPI docs ili ručno testiraj sa sledećim URL-ovima:

GET /

GET /fixtures?date=YYYY-MM-DD

GET /fixtures/today

GET /fixtures/yesterday

GET /fixtures/tomorrow

GET /fixtures/full-today

GET /fixtures/full-details?date=YYYY-MM-DD

GET /live

GET /odds/{fixture_id}

GET /predictions/{fixture_id}

GET /odds/live

GET /odds/live/bets

GET /odds?fixture=&league=&season=&date=YYYY-MM-DD

GET /leagues

GET /leagues/seasons

GET /standings/{league_id}

GET /teams?country=&league_id=&season=

GET /teams/statistics/{team_id}/{league_id}

GET /teams/countries

GET /players?team_id=&season=

GET /players/statistics/{player_id}/{league_id}

GET /players/topscorers/{league_id}

GET /players/topassists/{league_id}

GET /players/topyellowcards/{league_id}

GET /players/topredcards/{league_id}

GET /players/squads/{team_id}/{season}

GET /injuries?league_id=&ids=

GET /sidelined?players=&coaches=

GET /transfers/{player_id}

GET /coachs?team_id=&search=

GET /trophies?players=&coaches=

GET /test?date=YYYY-MM-DD

GET /teams/statistics/all

GET /standings/all

🧪 Testiranje
bash
Copy
Edit
pytest --cov=.

🐳 Docker

docker build -t today-api:latest .
docker run -p 10000:10000 \
  -e API_FOOTBALL_KEY=your_api_key \
  today-api:latest
  
☁️ Deploy na Render
Kreiraj render.yaml (već postoji) i runtime.txt (python-3.11.8).

Poveži repo, izaberi Docker ili Python environment.

Podesi env var:

API_FOOTBALL_KEY

Deploy!

🔮 Dalji razvoj
CI/CD (lint, tests, docker image publish)

Verzija API-ja (/api/v1/…)

Autentikacija & rate limiting

Prometheus metrics (/metrics)

Redis cache za redistribuciju

Monitoring i alerting

Pagination & filtering



