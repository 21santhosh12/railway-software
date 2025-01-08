from flask import Flask, jsonify, session
from config import SECRET_KEY, default_user_setup_done

# Import all the functions from routes package
from routes import (
    generate_admin_code,
    setup_default_user,
    index,
    register,
    login,
    admin_dashboard,
    generate_report,
    logout,
    home,
    handle_vehicle,
    calculate_charge,
    create_user,
    delete_user,
    admin_register,
    checkin,
    checkout,
    delete_admin,
    update_existing_admins,
    get_vehicle_suggestions
)

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Register all the routes with their respective functions
app.before_request(setup_default_user)

@app.route('/')
def route_index():
    return index()

@app.route('/register', methods=['GET', 'POST'])
def route_register():
    return register()

@app.route('/login', methods=['GET', 'POST'])
def route_login():
    return login()

@app.route('/admin_dashboard')
def route_admin_dashboard():
    return admin_dashboard()

@app.route('/generate_report', methods=['POST'])
def route_generate_report():
    return generate_report()

@app.route('/logout')
def route_logout():
    return logout()

@app.route('/home')
def route_home():
    return home()

@app.route('/handle_vehicle', methods=['POST'])
def route_handle_vehicle():
    return handle_vehicle()

@app.route('/route_create_user', methods=['POST'])
def route_create_user():
    return create_user()

@app.route('/route_delete_user/<username>', methods=['POST'])
def route_delete_user(username):
    try:
        if not session.get('is_admin'):
            return jsonify({'success': False, 'message': 'Unauthorized'})
        return delete_user(username)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin_register', methods=['GET', 'POST'])
def route_admin_register():
    return admin_register()

@app.route('/route_checkin', methods=['POST'])
def route_checkin():
    return checkin()

@app.route('/route_checkout', methods=['POST'])
def route_checkout():
    return checkout()

@app.route('/route_delete_admin/<username>', methods=['POST'])
def route_delete_admin(username):
    return delete_admin(username)

@app.route('/route_get_vehicle_suggestions')
def route_get_vehicle_suggestions():
    return get_vehicle_suggestions()

if __name__ == '__main__':
    update_existing_admins()
    app.run()
