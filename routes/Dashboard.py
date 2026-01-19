from flask import Blueprint, jsonify, request
from models import db, Industry, Waste, WasteRequest, waste_requests_schema

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")

@dashboard_bp.route("/stats", methods=["GET"])
def get_dashboard_stats():
    """Get overview statistics for the dashboard cards"""
    total_industries = Industry.query.count()
    total_waste_types = Waste.query.count()
    total_requests = WasteRequest.query.count()

    waste_totals = db.session.query(
        Waste.unit, db.func.sum(Waste.quantity)
    ).group_by(Waste.unit).all()

    total_waste_quantity = {unit: qty for unit, qty in waste_totals}

    return jsonify({
        "overview": {
            "total_industries": total_industries,
            "total_waste_types": total_waste_types,
            "total_requests": total_requests,
            "total_waste_quantity": total_waste_quantity
        }
    })

@dashboard_bp.route("/waste-requests", methods=["POST"])
def create_waste_request():
    """Submit a new waste request from the frontend"""
    data = request.get_json()

    # Basic Validation
    if not data or not data.get('industry_id') or not data.get('waste_id'):
        return jsonify({'error': 'Industry ID and Waste ID are required'}), 400

    # Verify that the industry and waste actually exist
    industry = Industry.query.get(data['industry_id'])
    waste = Waste.query.get(data['waste_id'])

    if not industry or not waste:
        return jsonify({'error': 'Selected Industry or Waste not found'}), 404

    # Create the record
    new_request = WasteRequest(
        quantity_requested=data.get('quantity_requested', 0.0),
        details=data.get('details', ''),
        status='pending', 
        industry_id=data['industry_id'],
        waste_id=data['waste_id']
    )

    db.session.add(new_request)
    db.session.commit()

    return jsonify({
        "message": "Waste request submitted successfully",
        "request_id": new_request.id
    }), 201

@dashboard_bp.route("/waste-requests", methods=["GET"])
def get_all_waste_requests():
    """Fetch all submitted requests for the 'Recent Requests' list"""
    # Using .desc() ensures new submissions appear at the top of your UI list
    all_requests = WasteRequest.query.order_by(WasteRequest.id.desc()).all()
    return waste_requests_schema.jsonify(all_requests)

@dashboard_bp.route("/waste-requests/<int:id>/status", methods=["PATCH"])
def update_request_status(id):
    """Approve or Reject a waste request and update inventory"""
    request_record = WasteRequest.query.get_or_404(id)
    data = request.get_json()

    if 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400

    new_status = data['status'].lower()

    # Logic: If approved, subtract requested quantity from the Waste stock
    if new_status == 'approved':
        waste_item = Waste.query.get(request_record.waste_id)
        
        if waste_item.quantity < request_record.quantity_requested:
            return jsonify({'error': 'Insufficient waste quantity in stock'}), 400
        
        waste_item.quantity -= request_record.quantity_requested

    request_record.status = new_status
    db.session.commit()

    return jsonify({
        "message": f"Request {new_status} successfully",
        "new_status": new_status
    })