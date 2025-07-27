from flask import Flask
from app.extensions import db, migrate  # ✅ Include migrate
from app.routes import register_routes
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)  # ✅ This line enables flask db commands

    register_routes(app)

    return app
