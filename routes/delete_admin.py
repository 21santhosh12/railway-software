from flask import session, redirect, url_for
from config import admins_collection

def delete_admin(username):
    if not session.get('is_admin'):
        return redirect(url_for('route_login'))
    
    # Prevent self-deletion and deletion of the main admin
    if username == session['username'] or username == 'admin':
        return redirect(url_for('route_admin_dashboard', 
                              error="Cannot delete your own account or the main admin account!"))
    
    admins_collection.delete_one({'username': username})
    return redirect(url_for('route_admin_dashboard', 
                          message='Admin user deleted successfully!')) 