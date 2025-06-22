#!/usr/bin/env python3
import httpx
import pycountry
from datetime import datetime
from typing import Any, Dict, List, Optional
import pytz

BASE_URL = "https://today-api-7f3i.onrender.com"


def fetch_fixtures(date: str) -> List[Dict[str, Any]]:
    """Povlači sve utakmice za dati datum."""
    r = httpx.get(f"{BASE_URL}/fixtures", params={"date": date}, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data.get("response", data)


def fetch_odds(date: str) -> List[Dict[str, Any]]:
    """Povlači sve odds zapise za dati datum."""
    r = httpx.get(f"{BASE_URL}/odds", params={"date": date}, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data.get("response", data)


def iso_to_local(iso: str) -> str:
    """Pretvara ISO-8601 (UTC) u lokalni string (Europe/Belgrade)."""
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return dt.strftime("%Y-%m-%d %H:%M")


def odd_to_pct(o: float) -> int:
    """Kvotu pretvara u procenat za BTTS yes."""
    try:
        return round((1 / o) * 100)
    except Exception:
        return 0


def country_flag(name: str) -> str:
    """Vraća emoji zastave na osnovu imena države."""
    try:
        c = pycountry.countries.lookup(name)
        return "".join(chr(0x1F1E6 + ord(ch) - ord("A")) for ch in c.alpha_2)
    except Exception:
        return ""


def flatten_bookmakers(fx: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Iz odds-objekta vadi listu bookmakera."""
    return fx.get("bookmakers", []) or []


def get_btts_yes_odd(fx: Dict[str, Any]) -> Optional[float]:
    """Izvlači kvotu za BTTS == Yes iz prvog dostupnog bookmakera."""
    for bm in flatten_bookmakers(fx):
        for bet in bm.get("bets", []) or []:
            if bet.get("name") in ("Both Teams Score", "Both Teams To Score"):
                for val in bet.get("values", []):
                    if val.get("value", "").lower() == "yes":
                        try:
                            return float(val.get("odd"))
                        except Exception:
                            return None
    return None


def main() -> None:
    tz = pytz.timezone("Europe/Belgrade")
    date_str = datetime.now(tz).strftime("%Y-%m-%d")

    fixtures = fetch_fixtures(date_str)
    # map fixture_id -> meta
    fixture_map = {f.get("fixture", {}).get("id"): f for f in fixtures}

    odds_list = fetch_odds(date_str)
    for fx in odds_list:
        fixture_id = fx.get("fixture", {}).get("id")
        meta = fixture_map.get(fixture_id)
        if not meta:
            continue  # nema podataka o meču

        yes_odd = get_btts_yes_odd(fx)
        if yes_odd is None:
            continue  # nema BTTS kvote

        yes_pct = odd_to_pct(yes_odd)
        no_pct = 100 - yes_pct

        league = meta.get("league", {})
        home = meta.get("teams", {}).get("home", {})
        away = meta.get("teams", {}).get("away", {})
        date_iso = meta.get("fixture", {}).get("date", "")

        print(f"🏟 League: {country_flag(league.get('country',''))} {league.get('country','')} — {league.get('name','')}")
        print(f"⚽ Match:  {home.get('name','')} vs {away.get('name','')}")
        print(f"⏰ Time:   {iso_to_local(date_iso)}\n")
        print("• BTTS:")
        print(f"    - Yes: {yes_pct}%")
        print(f"    - No:  {no_pct}%\n")

if __name__ == "__main__":
    main()
