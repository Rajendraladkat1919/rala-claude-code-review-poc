from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

# Deterministic mock readings for POC (no external API).
MOCK_BY_CITY_ID: dict[str, dict[str, str | float]] = {
    "mumbai": {"temperature_c": 30.0, "conditions": "Partly cloudy"},
    "delhi": {"temperature_c": 28.0, "conditions": "Haze"},
    "bengaluru": {"temperature_c": 24.0, "conditions": "Light rain"},
    "chennai": {"temperature_c": 32.0, "conditions": "Humid, clear"},
    "kolkata": {"temperature_c": 31.0, "conditions": "Thunderstorms nearby"},
    "hyderabad": {"temperature_c": 29.0, "conditions": "Clear"},
    "pune": {"temperature_c": 27.0, "conditions": "Pleasant, clear"},
    "ahmedabad": {"temperature_c": 33.0, "conditions": "Hot, sunny"},
    "jaipur": {"temperature_c": 30.0, "conditions": "Dry, sunny"},
    "lucknow": {"temperature_c": 26.0, "conditions": "Mist"},
    "kochi": {"temperature_c": 28.0, "conditions": "Heavy rain"},
    "indore": {"temperature_c": 25.0, "conditions": "Clear"},
}


@dataclass(frozen=True)
class WeatherSnapshot:
    city_name: str
    city_id: str
    temperature_c: float
    conditions: str
    local_datetime: datetime


class MockWeatherProvider:
    """Returns fixed mock weather for known Indian city ids."""

    def __init__(self, city_id_to_name: dict[str, str]) -> None:
        self._id_to_name = city_id_to_name

    def get_current(self, city_id: str) -> WeatherSnapshot:
        if city_id not in self._id_to_name:
            raise ValueError("Unknown city")
        row = MOCK_BY_CITY_ID.get(city_id)
        if not row:
            row = {"temperature_c": 26.0, "conditions": "Fair (mock default)"}

        return WeatherSnapshot(
            city_name=self._id_to_name[city_id],
            city_id=city_id,
            temperature_c=float(row["temperature_c"]),
            conditions=str(row["conditions"]),
            local_datetime=datetime.now(IST),
        )

# test comment
