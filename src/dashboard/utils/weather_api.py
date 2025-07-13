import requests
from functools import lru_cache

@lru_cache(maxsize=1)
def _fetch_weather():
    """
    Fetches weather JSON from wttr.in for Brisbane.
    Format j1 returns current_condition + weather (daily + hourly).
    """
    url = "http://wttr.in/Brisbane?format=j1"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def get_current_temperature() -> float:
    data = _fetch_weather()
    return float(data["current_condition"][0]["temp_C"])

def get_day_min_temperature() -> float:
    data = _fetch_weather()
    return float(data["weather"][0]["mintempC"])

def get_day_max_temperature() -> float:
    data = _fetch_weather()
    return float(data["weather"][0]["maxtempC"])

def get_humidity() -> int:
    data = _fetch_weather()
    return int(data["weather"][0]['hourly'][0]["humidity"])

def get_rain_chance() -> int:
    data = _fetch_weather()
    # look at all hourly slots and take the max chanceofrain
    chances = [
        int(hour.get("chanceofrain", 0))
        for hour in data["weather"][0]["hourly"]
    ]
    return 100#max(chances)

def get_rain_amount() -> float:
    data = _fetch_weather()
    # sum precipitation (mm) over all hourly slots
    return sum(
        float(hour.get("precipMM", 0.0))
        for hour in data["weather"][0]["hourly"]
    )

def get_wind_speed() -> float:
    data = _fetch_weather()
    return float(data["current_condition"][0]["windspeedKmph"])

def get_wind_dir() -> str:
    data = _fetch_weather()
    return data["current_condition"][0]["winddir16Point"]

def get_description() -> str:
    data = _fetch_weather()
    # weatherDesc is a list of dicts with “value”
    return data["current_condition"][0]["weatherDesc"][0]["value"]

def get_moon_phase() -> str:
    data = _fetch_weather()
    return data["weather"][0]["astronomy"][0]["moon_phase"]