from flask import Blueprint, flash, render_template, request

from app.data.indian_cities import CITY_IDS, INDIAN_CITIES
from app.services.weather import get_weather_provider

bp = Blueprint("weather", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    result = None
    selected = None

    if request.method == "POST":
        selected = request.form.get("city", "").strip()
        if not selected:
            flash("Please choose a city.", "error")
        elif selected not in CITY_IDS:
            flash("Invalid city selection.", "error")
            selected = None
        else:
            try:
                provider = get_weather_provider()
                result = provider.get_current(selected)
            except ValueError:
                flash("Could not load weather for that city.", "error")
                selected = None

    return render_template(
        "weather/index.html",
        cities=INDIAN_CITIES,
        result=result,
        selected_city=selected,
    )
