from flask import request, render_template, redirect, url_for, session
from config import admins_collection, users_collection

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        print(f"Login attempt for username: {username}")
        
        # First check admins collection
        admin = admins_collection.find_one({
            'username': username,
            'password': password
        })
        
        if admin:
            print(f"Admin login successful for {username}")
            session['username'] = admin['username']
            session['is_admin'] = True
            return redirect(url_for('route_admin_dashboard'))
        else:
            print(f"Admin login failed for {username}")
            
        # If not admin, check regular users collection
        user = users_collection.find_one({
            '$or': [
                {'username': username, 'password': password},
                {'email': username, 'password': password}
            ]
        })

        if user:
            print(f"User login successful for {username}")
            session['username'] = user['username']
            session['is_admin'] = False
            return redirect(url_for('route_home'))
        else:
            print(f"User login failed for {username}")
            
        return render_template('login.html', error='Invalid credentials!')

    return render_template('login.html') 