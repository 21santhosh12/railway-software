from flask import session, redirect, url_for

def index():
    if 'username' in session:
        if session.get('is_admin'):
            return redirect(url_for('route_admin_dashboard'))
        return redirect(url_for('route_home'))
    return redirect(url_for('route_login')) 