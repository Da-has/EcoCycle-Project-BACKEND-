from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

# Naming convention for Alembic migrations
metadata = MetaData()

# SQLAlchemy instance
db = SQLAlchemy(metadata=metadata)

# =======================
# User Model
# =======================
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = (
        '-waste_items.user',
        '-exchange_requests.user',
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.String, nullable=False)
    # producer | recycler | transporter | admin

    waste_items = db.relationship(
        'WasteItem',
        back_populates='user',
        cascade='all, delete'
    )

    exchange_requests = db.relationship(
        'ExchangeRequest',
        back_populates='user',
        cascade='all, delete'
    )

    def __repr__(self):
        return f'<User {self.id}, {self.name}, {self.role}>'


# =======================
# WasteItem Model
# =======================
class WasteItem(db.Model, SerializerMixin):
    __tablename__ = 'waste_items'

    serialize_rules = (
        '-user.waste_items',
        '-exchange_requests.waste_item',
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default='available')
    # available | requested | collected | recycled

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    user = db.relationship('User', back_populates='waste_items')

    exchange_requests = db.relationship(
        'ExchangeRequest',
        back_populates='waste_item',
        cascade='all, delete'
    )

    def __repr__(self):
        return f'<WasteItem {self.id}, {self.name}, {self.status}>'


# =======================
# ExchangeRequest Model
# =======================
class ExchangeRequest(db.Model, SerializerMixin):
    __tablename__ = 'exchange_requests'

    serialize_rules = (
        '-user.exchange_requests',
        '-waste_item.exchange_requests',
    )

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, default='pending')
    # pending | approved | rejected | completed

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    waste_item_id = db.Column(
        db.Integer,
        db.ForeignKey('waste_items.id'),
        nullable=False
    )

    user = db.relationship('User', back_populates='exchange_requests')
    waste_item = db.relationship('WasteItem', back_populates='exchange_requests')

    def __repr__(self):
        return f'<ExchangeRequest {self.id}, {self.status}>'

