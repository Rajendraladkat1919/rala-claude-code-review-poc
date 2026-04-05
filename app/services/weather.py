from flask import current_app

from app.data.indian_cities import INDIAN_CITIES
from app.services.mock_weather import MockWeatherProvider


def get_weather_provider():
    id_to_name = {c["id"]: c["name"] for c in INDIAN_CITIES}
    if current_app.config.get("USE_MOCK_WEATHER", True):
        return MockWeatherProvider(id_to_name)
    raise RuntimeError(
        "No HTTP weather provider configured; set USE_MOCK_WEATHER=true for POC."
    )
