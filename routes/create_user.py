from flask import request, jsonify, session
from datetime import datetime
from config import users_collection, rates_collection
from bson import ObjectId

def create_user():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})

    try:
        username = request.form.get('username')
        password = request.form.get('password')
        initial_amount = float(request.form.get('initial_amount', 15))
        initial_duration = float(request.form.get('initial_duration', 2))
        extra_charge = float(request.form.get('extra_charge', 10))
        extra_charge_duration = float(request.form.get('extra_charge_duration', 1))

        # Check if username already exists
        if users_collection.find_one({'username': username}):
            return jsonify({'success': False, 'message': 'Username already exists'})

        # Create rate document
        rate = {
            '_id': ObjectId(),
            'initial_amount': initial_amount,
            'initial_duration': initial_duration,
            'extra_charge': extra_charge,
            'extra_charge_duration': extra_charge_duration
        }

        # Create user document with reference to admin who created it
        user = {
            'username': username,
            'password': password,
            'rate_id': rate['_id'],
            'created_at': datetime.now(),
            'created_by': session['username']  # Store the admin who created this user
        }

        # Insert rate and user
        rates_collection.insert_one(rate)
        users_collection.insert_one(user)

        # Return success response with user data
        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'user': {
                'username': user['username'],
                'created_at': user['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
                'created_by': user['created_by'],
                'rate': {
                    'initial_amount': rate['initial_amount'],
                    'initial_duration': rate['initial_duration'],
                    'extra_charge': rate['extra_charge'],
                    'extra_charge_duration': rate['extra_charge_duration']
                }
            }
        })

    except Exception as e:
        print(f"Error creating user: {str(e)}")
        return jsonify({'success': False, 'message': f'Error creating user: {str(e)}'}) 