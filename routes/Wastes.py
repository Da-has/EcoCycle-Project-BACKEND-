from flask import Blueprint, request, jsonify
from models import db, Waste, waste_schema, wastes_schema, Industry

wastes_bp = Blueprint('wastes', __name__, url_prefix='/api/wastes')


@wastes_bp.route('', methods=['GET'])
def get_all_wastes():
    """Get all wastes"""
    industry_id = request.args.get('industry_id')

    if industry_id:
        wastes = Waste.query.filter_by(industry_id=industry_id).all()
    else:
        wastes = Waste.query.all()

    return wastes_schema.jsonify(wastes)


@wastes_bp.route('/<int:id>', methods=['GET'])
def get_waste(id):
    """Get a single waste by ID"""
    waste = Waste.query.get_or_404(id)
    return waste_schema.jsonify(waste)


@wastes_bp.route('', methods=['POST'])
def create_waste():
    """Create a new waste entry"""
    data = request.get_json()

    if not data or not data.get('name') or not data.get('wasteType') or not data.get('unit'):
        return jsonify({'error': 'Name, wasteType, and unit are required'}), 400

    if not data.get('industry_id'):
        return jsonify({'error': 'industry_id is required'}), 400

    industry = Industry.query.get(data['industry_id'])
    if not industry:
        return jsonify({'error': f'Industry with id {data["industry_id"]} not found'}), 404

    new_waste = Waste(
        name=data['name'],
        wasteType=data['wasteType'],
        quantity=data.get('quantity', 0.0),
        unit=data['unit'],
        notes=data.get('notes'),       
        industry_id=data['industry_id']
    )

    db.session.add(new_waste)
    db.session.commit()

    return waste_schema.jsonify(new_waste), 201


@wastes_bp.route('/<int:id>', methods=['PUT'])
def update_waste(id):
    """Update an existing waste entry"""
    waste = Waste.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'name' in data:
        waste.name = data['name']
    if 'wasteType' in data:
        waste.wasteType = data['wasteType']
    if 'quantity' in data:
        waste.quantity = data['quantity']
    if 'unit' in data:
        waste.unit = data['unit']
    if 'notes' in data:               
        waste.notes = data['notes']

    if 'industry_id' in data:
        industry = Industry.query.get(data['industry_id'])
        if not industry:
            return jsonify({'error': f'Industry with id {data["industry_id"]} not found'}), 404
        waste.industry_id = data['industry_id']

    db.session.commit()
    return waste_schema.jsonify(waste)


@wastes_bp.route('/<int:id>', methods=['DELETE'])
def delete_waste(id):
    """Delete a waste entry"""
    waste = Waste.query.get_or_404(id)
    db.session.delete(waste)
    db.session.commit()

    return jsonify({'message': f'Waste {id} deleted successfully'})


@wastes_bp.route('/type/<waste_type>', methods=['GET'])
def get_wastes_by_type(waste_type):
    """Get all wastes of a specific type"""
    wastes = Waste.query.filter_by(wasteType=waste_type).all()
    return wastes_schema.jsonify(wastes)


@wastes_bp.route('/available', methods=['GET'])
def get_available_wastes():
    """Get all wastes with quantity > 0"""
    wastes = Waste.query.filter(Waste.quantity > 0).all()
    return wastes_schema.jsonify(wastes)


@wastes_bp.route('/total-quantity', methods=['GET'])
def get_total_quantity():
    """Get total quantity of all wastes"""
    from sqlalchemy import func

    result = db.session.query(
        func.sum(Waste.quantity),
        func.count(Waste.id)
    ).first()

    return jsonify({
        'total_quantity': result[0] or 0,
        'total_types': result[1] or 0
    })


@wastes_bp.route('/count', methods=['GET'])
def get_waste_count():
    """Get total count of waste entries"""
    count = Waste.query.count()
    return jsonify({'count': count})
