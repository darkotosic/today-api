from pydantic import BaseModel

class Fixture(BaseModel):
    league: str
    home_team: str
    away_team: str
    start_time: str
