from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from models import db, ma
from flask import Flask
from flask_migrate import Migrate

# Import route blueprints
from routes.Industries import industries_bp
from routes.Wastes import wastes_bp
from routes.Dashboard import dashboard_bp

# Create a flask application object
app = Flask(__name__)

# Configure a database connection to the local file ecocycle.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecocycle.db'

# Disable modification tracking to use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db.init_app(app)

# Initialize Marshmallow with the app
ma.init_app(app)

# Create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# Register route blueprints
app.register_blueprint(industries_bp)
app.register_blueprint(wastes_bp)
app.register_blueprint(dashboard_bp)


# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'message': 'EcoCycle API is running'}


if __name__ == '__main__':
    app.run(port=5555, debug=True)

