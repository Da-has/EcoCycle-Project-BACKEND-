from flask import Blueprint, request, jsonify
from models import db, Industry, industry_schema, industries_schema

# Create Blueprint for industries routes
industries_bp = Blueprint('industries', __name__, url_prefix='/api/industries')


@industries_bp.route('', methods=['GET'])
def get_all_industries():
    """Get all industries"""
    all_industries = Industry.query.all()
    return industries_schema.jsonify(all_industries)


@industries_bp.route('/<int:id>', methods=['GET'])
def get_industry(id):
    """Get a single industry by ID"""
    industry = Industry.query.get_or_404(id)
    return industry_schema.jsonify(industry)


@industries_bp.route('', methods=['POST'])
def create_industry():
    """Create a new industry"""
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('name') or not data.get('industry_code'):
        return jsonify({'error': 'Name and industry_code are required'}), 400
    
    # Check if industry_code already exists
    existing = Industry.query.filter_by(industry_code=data['industry_code']).first()
    if existing:
        return jsonify({'error': f'Industry with code {data["industry_code"]} already exists'}), 400
    
    new_industry = Industry(
        name=data['name'],
        industry_code=data['industry_code'],
        description=data.get('description', '')
    )
    
    db.session.add(new_industry)
    db.session.commit()
    
    return industry_schema.jsonify(new_industry), 201


@industries_bp.route('/<int:id>', methods=['PUT'])
def update_industry(id):
    """Update an existing industry"""
    industry = Industry.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields if provided
    if 'name' in data:
        industry.name = data['name']
    if 'industry_code' in data:
        # Check if new code is already taken by another industry
        existing = Industry.query.filter(
            Industry.industry_code == data['industry_code'],
            Industry.id != id
        ).first()
        if existing:
            return jsonify({'error': f'Industry with code {data["industry_code"]} already exists'}), 400
        industry.industry_code = data['industry_code']
    if 'description' in data:
        industry.description = data['description']
    
    db.session.commit()
    
    return industry_schema.jsonify(industry)


@industries_bp.route('/<int:id>', methods=['DELETE'])
def delete_industry(id):
    """Delete an industry"""
    industry = Industry.query.get_or_404(id)
    
    # Note: Due to cascade, related wastes and waste_requests will also be deleted
    db.session.delete(industry)
    db.session.commit()
    
    return jsonify({'message': f'Industry {id} deleted successfully'})


# Additional utility endpoints

@industries_bp.route('/search', methods=['GET'])
def search_industries():
    """Search industries by name"""
    query = request.args.get('q', '')
    industries = Industry.query.filter(Industry.name.ilike(f'%{query}%')).all()
    return industries_schema.jsonify(industries)


@industries_bp.route('/count', methods=['GET'])
def get_industry_count():
    """Get total count of industries"""
    count = Industry.query.count()
    return jsonify({'count': count})

