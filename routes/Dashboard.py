from flask import Blueprint, request, jsonify
from models import db, Industry, Waste, WasteRequest, waste_request_schema, waste_requests_schema
from sqlalchemy import func

# Create Blueprint for dashboard routes
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


@dashboard_bp.route('/stats', methods=['GET'])
def get_dashboard_stats():
    """Get aggregated statistics for the dashboard"""
    # Count industries
    industry_count = Industry.query.count()
    
    # Count wastes
    waste_count = Waste.query.count()
    
    # Count waste requests
    request_count = WasteRequest.query.count()
    
    # Count by status
    pending_count = WasteRequest.query.filter_by(status='pending').count()
    approved_count = WasteRequest.query.filter_by(status='approved').count()
    rejected_count = WasteRequest.query.filter_by(status='rejected').count()
    
    # Total waste quantity
    total_quantity = db.session.query(func.sum(Waste.quantity)).scalar() or 0
    
    # Wastes by type distribution
    waste_by_type = db.session.query(
        Waste.wasteType,
        func.count(Waste.id),
        func.sum(Waste.quantity)
    ).group_by(Waste.wasteType).all()
    
    type_distribution = [
        {
            'type': w[0],
            'count': w[1],
            'total_quantity': w[2] or 0
        }
        for w in waste_by_type
    ]
    
    # Industries with most waste
    top_industries = db.session.query(
        Industry.name,
        func.count(Waste.id).label('waste_count'),
        func.sum(Waste.quantity).label('total_quantity')
    ).join(Waste).group_by(Industry.id).order_by(
        func.count(Waste.id).desc()
    ).limit(5).all()
    
    industries_data = [
        {
            'name': i[0],
            'waste_count': i[1],
            'total_quantity': i[2] or 0
        }
        for i in top_industries
    ]
    
    return jsonify({
        'overview': {
            'total_industries': industry_count,
            'total_waste_types': waste_count,
            'total_requests': request_count,
            'total_waste_quantity': total_quantity
        },
        'request_status': {
            'pending': pending_count,
            'approved': approved_count,
            'rejected': rejected_count
        },
        'waste_by_type': type_distribution,
        'top_industries': industries_data
    })


@dashboard_bp.route('/waste-requests', methods=['GET'])
def get_all_waste_requests():
    """Get all waste requests with optional filtering"""
    # Optional filter by status
    status = request.args.get('status')
    
    if status:
        requests = WasteRequest.query.filter_by(status=status).all()
    else:
        requests = WasteRequest.query.all()
    
    return waste_requests_schema.jsonify(requests)


@dashboard_bp.route('/waste-requests/<int:id>', methods=['GET'])
def get_waste_request(id):
    """Get a single waste request by ID"""
    request = WasteRequest.query.get_or_404(id)
    return waste_request_schema.jsonify(request)


@dashboard_bp.route('/waste-requests/<int:id>', methods=['PUT'])
def update_waste_request(id):
    """Update waste request status"""
    waste_request = WasteRequest.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update status if provided
    if 'status' in data:
        new_status = data['status']
        valid_statuses = ['pending', 'approved', 'rejected']
        
        if new_status not in valid_statuses:
            return jsonify({'error': f'Invalid status. Must be one of: {valid_statuses}'}), 400
        
        waste_request.status = new_status
    
    # Update details if provided
    if 'details' in data:
        waste_request.details = data['details']
    
    # Update quantity if provided
    if 'quantity_requested' in data:
        waste_request.quantity_requested = data['quantity_requested']
    
    db.session.commit()
    
    return waste_request_schema.jsonify(waste_request)


@dashboard_bp.route('/waste-requests/<int:id>/approve', methods=['PUT'])
def approve_waste_request(id):
    """Approve a waste request"""
    waste_request = WasteRequest.query.get_or_404(id)
    
    if waste_request.status != 'pending':
        return jsonify({'error': 'Only pending requests can be approved'}), 400
    
    waste_request.status = 'approved'
    db.session.commit()
    
    return waste_request_schema.jsonify(waste_request)


@dashboard_bp.route('/waste-requests/<int:id>/reject', methods=['PUT'])
def reject_waste_request(id):
    """Reject a waste request"""
    waste_request = WasteRequest.query.get_or_404(id)
    
    if waste_request.status != 'pending':
        return jsonify({'error': 'Only pending requests can be rejected'}), 400
    
    waste_request.status = 'rejected'
    db.session.commit()
    
    return waste_request_schema.jsonify(waste_request)


@dashboard_bp.route('/waste-requests', methods=['POST'])
def create_waste_request():
    """Create a new waste request"""
    from models import Industry, Waste
    
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('industry_id') or not data.get('waste_id'):
        return jsonify({'error': 'industry_id and waste_id are required'}), 400
    
    if not data.get('quantity_requested') or data['quantity_requested'] <= 0:
        return jsonify({'error': 'quantity_requested must be a positive number'}), 400
    
    # Validate industry exists
    industry = Industry.query.get(data['industry_id'])
    if not industry:
        return jsonify({'error': f'Industry with id {data["industry_id"]} not found'}), 404
    
    # Validate waste exists
    waste = Waste.query.get(data['waste_id'])
    if not waste:
        return jsonify({'error': f'Waste with id {data["waste_id"]} not found'}), 404
    
    new_request = WasteRequest(
        quantity_requested=data['quantity_requested'],
        status='pending',
        details=data.get('details', ''),
        industry_id=data['industry_id'],
        waste_id=data['waste_id']
    )
    
    db.session.add(new_request)
    db.session.commit()
    
    return waste_request_schema.jsonify(new_request), 201


@dashboard_bp.route('/waste-requests/<int:id>', methods=['DELETE'])
def delete_waste_request(id):
    """Delete a waste request"""
    waste_request = WasteRequest.query.get_or_404(id)
    
    db.session.delete(waste_request)
    db.session.commit()
    
    return jsonify({'message': f'Waste request {id} deleted successfully'})


@dashboard_bp.route('/recent-activity', methods=['GET'])
def get_recent_activity():
    """Get recent waste requests (last 10)"""
    recent_requests = WasteRequest.query.order_by(
        WasteRequest.id.desc()
    ).limit(10).all()
    
    return waste_requests_schema.jsonify(recent_requests)

