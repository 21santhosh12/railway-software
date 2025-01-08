from flask import session, redirect, url_for

def logout():
    session.pop('username', None)
    session.pop('is_admin', None)
    return redirect(url_for('route_login')) 