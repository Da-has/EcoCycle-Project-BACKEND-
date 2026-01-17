from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from models import db
from flask import Flask
from flask_migrate import Migrate


# create a flask application object
app = Flask(__name__)

# confogure a database connection to the local file ecocycle.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecocycle.db'

# disable modification tracking to use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# initialize the Flask application to use the database
db.init_app(app)



if __name__ == '__main__':
    app.run(port=5555, debug=True)