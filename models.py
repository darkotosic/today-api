from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class FixtureInfo(BaseModel):
    id: int = Field(..., alias="id")
    referee: Optional[str] = Field(None, alias="referee")
    timezone: str = Field(..., alias="timezone")
    date: datetime = Field(..., alias="date")
    venue: Dict[str, Any] = Field(..., alias="venue")
    status: Dict[str, Any] = Field(..., alias="status")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class TeamInfo(BaseModel):
    id: int = Field(..., alias="id")
    name: str = Field(..., alias="name")
    logo: Optional[str] = Field(None, alias="logo")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Teams(BaseModel):
    home: TeamInfo = Field(..., alias="home")
    away: TeamInfo = Field(..., alias="away")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class LeagueInfo(BaseModel):
    id: int = Field(..., alias="id")
    name: str = Field(..., alias="name")
    country: Optional[str] = Field(None, alias="country")
    logo: Optional[str] = Field(None, alias="logo")
    season: int = Field(..., alias="season")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Event(BaseModel):
    time: Dict[str, Any] = Field(..., alias="time")
    team: Dict[str, Any] = Field(..., alias="team")
    player: Dict[str, Any] = Field(..., alias="player")
    type: str = Field(..., alias="type")
    detail: Optional[str] = Field(None, alias="detail")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Lineup(BaseModel):
    team: Dict[str, Any] = Field(..., alias="team")
    coach: Dict[str, Any] = Field(..., alias="coach")
    formation: Optional[str] = Field(None, alias="formation")
    startXI: List[Dict[str, Any]] = Field(..., alias="startXI")
    substitutes: List[Dict[str, Any]] = Field(..., alias="substitutes")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class StatisticEntry(BaseModel):
    type: str = Field(..., alias="type")
    value: Any = Field(..., alias="value")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Prediction(BaseModel):
    # uses raw dict for flexibility
    response: List[Dict[str, Any]] = Field(..., alias="response")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Odds(BaseModel):
    response: List[Dict[str, Any]] = Field(..., alias="response")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class HeadToHead(BaseModel):
    response: List[Dict[str, Any]] = Field(..., alias="response")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class FixtureEnriched(BaseModel):
    fixture: FixtureInfo = Field(..., alias="fixture")
    league: LeagueInfo = Field(..., alias="league")
    teams: Teams = Field(..., alias="teams")
    events: Optional[List[Event]] = Field(default_factory=list, alias="events")
    lineups: Optional[List[Lineup]] = Field(default_factory=list, alias="lineups")
    statistics: Optional[List[StatisticEntry]] = Field(default_factory=list, alias="statistics")
    h2h: Optional[List[Dict[str, Any]]] = Field(default_factory=list, alias="h2h")
    predictions: List[Dict[str, Any]] = Field(default_factory=list, alias="predictions")
    odds: List[Dict[str, Any]] = Field(default_factory=list, alias="odds")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class FixturesResponse(BaseModel):
    response: List[FixtureEnriched] = Field(..., alias="response")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class LeagueSeasons(BaseModel):
    league: LeagueInfo = Field(..., alias="league")
    seasons: List[Dict[str, Any]] = Field(..., alias="seasons")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class LeaguesResponse(BaseModel):
    response: List[LeagueSeasons] = Field(..., alias="response")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class TeamDetails(BaseModel):
    team: TeamInfo = Field(..., alias="team")
    statistics: Optional[List[StatisticEntry]] = Field(default_factory=list, alias="statistics")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class TeamsResponse(BaseModel):
    response: List[Dict[str, Any]] = Field(..., alias="response")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class StandingsResponse(BaseModel):
    response: List[Dict[str, Any]] = Field(..., alias="response")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
