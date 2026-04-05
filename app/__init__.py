import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from app.config import config_by_name

csrf = CSRFProtect()


def create_app(config_name: str | None = None) -> Flask:
    name = config_name or os.getenv("FLASK_ENV", "development")
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    app.config.from_object(config_by_name[name])
    csrf.init_app(app)

    from app.blueprints.weather import bp as weather_bp

    app.register_blueprint(weather_bp)

    return app
