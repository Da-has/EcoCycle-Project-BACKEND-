from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_marshmallow import Marshmallow

# Definition of tables and associated schema constructs
metadata = MetaData()

# Create the Flask SQLAlchemy extension
db = SQLAlchemy(metadata=metadata)

# Create Marshmallow extension for serialization
ma = Marshmallow()


# ==========================================
# Database Models
# ==========================================

class Industry(db.Model):
    __tablename__ = "industries"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    industry_code = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.Text())

    # Relationships
    wastes = db.relationship('Waste', backref='industry', lazy=True, cascade="all, delete-orphan")
    waste_requests = db.relationship('WasteRequest', backref='industry', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Industry {self.name}>'


class Waste(db.Model):
    __tablename__ = "wastes"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    wasteType = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Float(), default=0.0)
    unit = db.Column(db.String(20), nullable=False)

    # Foreign Key to Industry
    industry_id = db.Column(db.Integer(), db.ForeignKey('industries.id'), nullable=False)

    # Relationships
    waste_requests = db.relationship('WasteRequest', backref='waste', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Waste {self.name}>'


class WasteRequest(db.Model):
    __tablename__ = "wasteRequests"

    id = db.Column(db.Integer(), primary_key=True)
    quantity_requested = db.Column(db.Float(), default=0.0)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    details = db.Column(db.Text())

    # Foreign Keys
    industry_id = db.Column(db.Integer(), db.ForeignKey('industries.id'), nullable=False)
    waste_id = db.Column(db.Integer(), db.ForeignKey('wastes.id'), nullable=False)

    def __repr__(self):
        return f'<WasteRequest {self.status}>'


# ==========================================
# Marshmallow Schemas for Serialization
# ==========================================

class IndustrySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'industry_code', 'description', 'wastes', 'waste_requests')
    
    wastes = ma.List(ma.Nested('WasteSchema', exclude=('industry',)))
    waste_requests = ma.List(ma.Nested('WasteRequestSchema', exclude=('industry', 'waste',)))


class WasteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'wasteType', 'quantity', 'unit', 'industry_id', 'industry', 'waste_requests')
    
    industry = ma.Nested('IndustrySchema', only=('id', 'name', 'industry_code'))
    waste_requests = ma.List(ma.Nested('WasteRequestSchema', exclude=('industry', 'waste',)))


class WasteRequestSchema(ma.Schema):
    class Meta:
        fields = ('id', 'quantity_requested', 'status', 'details', 'industry_id', 'waste_id', 'industry', 'waste')
    
    industry = ma.Nested('IndustrySchema', only=('id', 'name'))
    waste = ma.Nested('WasteSchema', only=('id', 'name', 'wasteType'))


# ==========================================
# Schema Instances (for serialization)
# ==========================================

industry_schema = IndustrySchema()
industries_schema = IndustrySchema(many=True)

waste_schema = WasteSchema()
wastes_schema = WasteSchema(many=True)

waste_request_schema = WasteRequestSchema()
waste_requests_schema = WasteRequestSchema(many=True)

