"""WSGI entry for Gunicorn: gunicorn -w 2 -b 127.0.0.1:8000 wsgi:app"""

import os

from dotenv import load_dotenv

load_dotenv()

from app import create_app

config = os.getenv("FLASK_ENV", "development")
app = create_app(config)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=config == "development")
