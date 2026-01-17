from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

#definition of tables and associated schema constructs
metadata = MetaData()

#create the Flask SQLAlchemy extension
db = SQLAlchemy(metadata=metadata)

# Model the tables

class Industry(db.Model):
    __tablename__ = "industries"

    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.Text(), nullable = False)
    industry_code = db.Column(db.Integer())
    description = db.Column(db.Text())

    #define relationships





class Waste(db.Model):
    __tablename__ = "wastes"
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.Text(), nullable = False)
    wasteType = db.Column(db.Text(), nullable = False)
    Quantity = db.Column(db.Float())
    Unit = db.Column(db.Text(), nullable = False)

    # Define relationship here
    # industry_id = db.Column(db.Integer(), )
    



class WasteRequest(db.Model):
    __tablename__ = "wasteRequests"
    id = db.Column(db.Integer(), primary_key = True)
    quantity_requested = db.Column(db.Float())
    status = db.Column(db.Text())
    details = db.Column(db.Text())

    # Define relationships here


