from flask import request, jsonify, session
from config import vehicles_collection

def get_vehicle_suggestions():
    query = request.args.get('query', '').upper()
    if len(query) < 2:
        return jsonify({'suggestions': []})
    
    # Get current user's username
    handler_username = session.get('username')
    
    # Find vehicles that match the query AND were handled by this user
    vehicles = vehicles_collection.find(
        {
            'vehicle_number': {'$regex': f'^{query}'},
            'handled_by': handler_username,  # Add this condition
            'checkout_time': None  # Only show active vehicles
        },
        {'vehicle_number': 1, '_id': 0}
    ).limit(5)  # Limit to 5 suggestions
    
    suggestions = [v['vehicle_number'] for v in vehicles]
    return jsonify({'suggestions': suggestions}) 