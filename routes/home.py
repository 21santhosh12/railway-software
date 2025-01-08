from flask import session, redirect, url_for, render_template

def home():
    if 'username' not in session:
        return redirect(url_for('route_login'))
    return render_template('home.html', username=session['username']) 