import os  # 1. Added os import
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, ma

from routes.Industries import industries_bp
from routes.Wastes import wastes_bp
from routes.Dashboard import dashboard_bp

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecocycle.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(industries_bp)
app.register_blueprint(wastes_bp)
app.register_blueprint(dashboard_bp)

@app.route("/api/health", methods=["GET"])
def health_check():
    return {"status": "healthy", "message": "EcoCycle API is running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5555))
    app.run(host="0.0.0.0", port=port, debug=True)