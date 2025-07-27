from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_jwt_extended import JWTManager  # ✅ Add JWTManager
from app.extensions import db, migrate
from app.models import *
from app.routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    # ✅ Initialize JWT
    jwt = JWTManager(app)

    register_routes(app)

    return app

app = create_app()

# ✅ Debug: Print registered routes
with app.app_context():
    print("\n🔍 Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(rule)

if __name__ == '__main__':
    app.run(debug=True)
