from pydantic import BaseModel, Field

class Location(BaseModel):
    latitude: float
    longitude: float
    name: str | None = None
    timezone: str | None = None

class CurrentConditions(BaseModel):
    temperature_c: float
    feels_like_c: float
    humidity_pct: float
    wind_speed_kph: float
    wind_direction_deg: float
    pressure_hpa: float
    condition_code: int
    condition_text: str
    observed_at: str # ISO 8601
    is_day: bool

class HourlyForecastEntry(BaseModel):
    time: str # ISO 8601
    temperature_c: float
    precipitation_probability_pct: float | None = None
    condition_code: int
    condition_text: str
    wind_speed_kph: float

class DailyForecastEntry(BaseModel):
    date: str # YYY-MM-DD
    temperature_max_c: float
    temperature_min_c: float
    precipitation__probability_pct: float | None = None
    condition_code: int
    condition_text: str
    sunrise: str | None = None
    sunset: str | None = None


class CurrentConditionsResponse(BaseModel):
    location: Location
    current: CurrentConditions
    source: str = Field(description="Upstream provider that served this data")
    cached: bool = False

class HourlyForecastResponse(BaseModel):
    location: Location
    hourly: list[HourlyForecastEntry]
    source: str
    cached: bool = False

class DailyForecastResponse(BaseModel):
    location: Location
    daily: list[DailyForecastEntry]
    source: str
    cached: bool = False

class GeocodeResult(BaseModel):
    name: str
    latitude: float
    longitude: float
    country: str | None = None
    admin1: str | None = None # state/region

class SearchResponse(BaseModel):
    results: list[GeocodeResult]