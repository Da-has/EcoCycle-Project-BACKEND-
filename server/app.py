from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db

def create_app():
    app = Flask(__name__)

    # Database config
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.json.compact = False

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)

    # ------------------------
    # Routes
    # ------------------------

    @app.route("/")
    def index():
        return make_response(
            {"message": "EcoCycle API running"}, 200
        )

    return app


# Create app instance
app = create_app()

if __name__ == "__main__":
    app.run(port=5555, debug=True)
