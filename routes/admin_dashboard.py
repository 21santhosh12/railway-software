from flask import session, redirect, url_for, render_template
from datetime import datetime
from config import users_collection, admins_collection, vehicles_collection

def admin_dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('route_login'))
    
    current_admin = session['username']
    
    # Get only users created by this admin
    regular_users = list(users_collection.aggregate([
        {
            '$match': {
                'created_by': current_admin  # Only get users created by current admin
            }
        },
        {
            '$lookup': {
                'from': 'rates',
                'localField': 'rate_id',
                'foreignField': '_id',
                'as': 'rate'
            }
        },
        {
            '$unwind': {
                'path': '$rate',
                'preserveNullAndEmptyArrays': True
            }
        },
        {
            '$sort': {'created_at': -1}
        }
    ]))
    
    # Get active vehicles only for users created by this admin
    active_vehicles = list(vehicles_collection.find({
        'handled_by': {'$in': [user['username'] for user in regular_users]},
        'checkout_time': None
    }).sort('checkin_time', -1))
    
    # Get admin users
    admin_users = list(admins_collection.find().sort('created_at', -1))
    
    # Get total users count for this admin
    total_users = len(regular_users)
    
    # Get today's check-ins count for users created by this admin
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    todays_checkins = vehicles_collection.count_documents({
        'handled_by': {'$in': [user['username'] for user in regular_users]},
        'checkin_time': {'$gte': today_start}
    })

    return render_template('admin_dashboard.html',
                         regular_users=regular_users,
                         admin_users=admin_users,
                         active_vehicles=active_vehicles,
                         current_user=current_admin,
                         total_users=total_users,
                         todays_checkins=todays_checkins) 