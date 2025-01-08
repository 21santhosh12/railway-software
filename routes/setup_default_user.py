from flask import request, redirect, url_for, flash
from config import admins_collection, default_user_setup_done

def setup_default_user():
    global default_user_setup_done
    if not default_user_setup_done:
        # Check if any admin exists
        admin_exists = admins_collection.find_one({})
        if not admin_exists:
            # Don't create default admin, just set the flag
            default_user_setup_done = True
            # If trying to access any route except admin_register, redirect to it
            if request.endpoint and request.endpoint not in ['route_admin_register', 'static']:
                flash('No admin exists. Please create an admin account using the master key.', 'warning')
                return redirect(url_for('route_admin_register')) 