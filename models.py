from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_marshmallow import Marshmallow

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)
ma = Marshmallow()

class Industry(db.Model):
    __tablename__ = "industries"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    industry_code = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.Text())

    wastes = db.relationship('Waste', backref='industry', lazy=True, cascade="all, delete-orphan")
    waste_requests = db.relationship('WasteRequest', backref='industry', lazy=True, cascade="all, delete-orphan")

class Waste(db.Model):
    __tablename__ = "wastes"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    wasteType = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Float(), default=0.0)
    unit = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text()) 
    industry_id = db.Column(db.Integer(), db.ForeignKey('industries.id'), nullable=False)

    waste_requests = db.relationship('WasteRequest', backref='waste', lazy=True, cascade="all, delete-orphan")

class WasteRequest(db.Model):
    __tablename__ = "wasteRequests"
    id = db.Column(db.Integer(), primary_key=True)
    quantity_requested = db.Column(db.Float(), default=0.0)
    status = db.Column(db.String(20), default='pending')
    details = db.Column(db.Text())
    industry_id = db.Column(db.Integer(), db.ForeignKey('industries.id'), nullable=False)
    waste_id = db.Column(db.Integer(), db.ForeignKey('wastes.id'), nullable=False)

class WasteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Waste
        load_instance = True
        include_fk = True
    industry = ma.Nested('IndustrySchema', only=('id', 'name'))
    waste_requests = ma.List(ma.Nested('WasteRequestSchema', exclude=('waste',)))

class IndustrySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Industry
        load_instance = True
    wastes = ma.List(ma.Nested(WasteSchema, exclude=('industry', 'waste_requests')))
    waste_requests = ma.List(ma.Nested('WasteRequestSchema', exclude=('industry',)))

class WasteRequestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WasteRequest
        load_instance = True
        include_fk = True
    waste = ma.Nested(WasteSchema, only=('id', 'name', 'wasteType'))
    industry = ma.Nested(IndustrySchema, only=('id', 'name'))

industry_schema = IndustrySchema()
industries_schema = IndustrySchema(many=True)
waste_schema = WasteSchema()
wastes_schema = WasteSchema(many=True)
waste_request_schema = WasteRequestSchema()
waste_requests_schema = WasteRequestSchema(many=True)