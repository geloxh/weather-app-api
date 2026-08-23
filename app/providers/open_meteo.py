""" 
Open-Meteo emplementation of WeatherProvider.
Docs: https://open-meteo.com/en/docs
No API key required — Initial provider.
"""

import httpx

from app.config import get_settings
from app.models.schemas import (
    CurrentConditions,
    DailyForecastEntry,
    GeocodeResult,
    HourlyForecastEntry,
)
from app..providers.base import WeatherProvider

settings = get_settings()

### WMO Weather interpretation codes -> human readable text
WMO_CODES: dict[int, str] = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight show",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
}