from flask import jsonify
from config import db

def delete_user(username):
    try:
        # First find the user to get their rate
        user = db.users.find_one({'username': username, 'is_admin': False})
        if not user:
            return jsonify({
                'success': False,
                'message': f'User {username} not found'
            })
            
        # Delete the rate first
        db.rates.delete_one({'username': username})
            
        # Then delete the user
        result = db.users.delete_one({'username': username, 'is_admin': False})
        
        if result.deleted_count > 0:
            return jsonify({
                'success': True,
                'message': f'User {username} deleted successfully'
            })
        
        return jsonify({
            'success': False,
            'message': f'Failed to delete user {username}'
        })
            
    except Exception as e:
        print(f"Error deleting user: {str(e)}")  # For debugging
        return jsonify({
            'success': False,
            'message': f'Error deleting user: {str(e)}'
        }) 