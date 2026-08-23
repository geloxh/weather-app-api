"""Abstract base class for weather providers."""

from abc import ABC, abstractmethod

from app.models.schemas import {
    CurrentConditions,
    DailyForecastEntry,
    GeocodeResult,
    HourlyForecastEntry,
}

class WeatherProvider(ABC):
    name: str = "base"

    @abstractmethod
    async def get_current(self, lat: float, lon: float) -> CurrentConditions:
        ...
    abstractmethod
    async def get_hourly_forecast(
        self, lat: float, lon: float, hours: int = 48
    ) -> list[HourlyForecastEntry]:
        ...

    @abstractmethod
    async def get_daily_forecast(
        self, lat: float, lon: float, days: int = 7
    ) -> list[DailyForecastEntry]:
        ...

    @abstractmethod
    async def get_daily_forecast(
        self, lat: float, lon: float, days: int = 7
    ) -> list[DailyForecastEntry]:
        ...

    @abstractmethod
    async def geocode(self, query: str) -> list[GeoCodeResult]
        ...