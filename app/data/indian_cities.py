"""Curated Indian cities for the POC dropdown (value = stable id for mock lookup)."""

INDIAN_CITIES = [
    {"id": "mumbai", "name": "Mumbai"},
    {"id": "delhi", "name": "Delhi"},
    {"id": "bengaluru", "name": "Bengaluru"},
    {"id": "chennai", "name": "Chennai"},
    {"id": "kolkata", "name": "Kolkata"},
    {"id": "hyderabad", "name": "Hyderabad"},
    {"id": "pune", "name": "Pune"},
    {"id": "ahmedabad", "name": "Ahmedabad"},
    {"id": "jaipur", "name": "Jaipur"},
    {"id": "lucknow", "name": "Lucknow"},
    {"id": "kochi", "name": "Kochi"},
    {"id": "indore", "name": "Indore"},
]

CITY_IDS = {c["id"] for c in INDIAN_CITIES}
