from flask import session, redirect, url_for, request, jsonify
from datetime import datetime
from config import users_collection, rates_collection, vehicles_collection

def checkin():
    if 'username' not in session:
        return redirect(url_for('route_login'))
    
    try:
        vehicle_number = request.form['vehicle_number'].upper()
        payment_mode = request.form['payment_mode']
        handler_username = session['username']
        
        # Get the user and their rate
        user = users_collection.find_one({'username': handler_username})
        if not user:
            return jsonify({
                'error': True,
                'message': 'User not found!'
            })
            
        rate = rates_collection.find_one({'_id': user['rate_id']})
        if not rate:
            return jsonify({
                'error': True,
                'message': 'Rate configuration not found!'
            })
        
        # Check if vehicle is already checked in by THIS user
        existing_vehicle = vehicles_collection.find_one({
            'vehicle_number': vehicle_number,
            'handled_by': handler_username,
            'checkout_time': None
        })
        
        if existing_vehicle:
            return jsonify({
                'error': True,
                'message': f'Vehicle {vehicle_number} is already checked in under your account!'
            })
        
        # Create new check-in record
        checkin_time = datetime.now()
        vehicles_collection.insert_one({
            'vehicle_number': vehicle_number,
            'checkin_time': checkin_time,
            'checkout_time': None,
            'payment_mode': payment_mode,
            'handled_by': handler_username,
            'rate_id': rate['_id']
        })
        
        # Use existing receipt HTML format but with dynamic values
        receipt_html = f'''
        <div class="receipt-container" id="checkinReceipt">
            <div class="receipt">
                <div class="receipt-header">
                    <h2>PARKING TICKET</h2>
                    <div class="receipt-divider"></div>
                </div>
                
                <div class="receipt-body">
                    <div class="receipt-row">
                        <span>Vehicle:</span>
                        <span>{vehicle_number}</span>
                    </div>
                    
                    <div class="receipt-row">
                        <span>In:</span>
                        <span>{checkin_time.strftime('%H:%M %d/%m')}</span>
                    </div>
                    
                    <div class="receipt-divider"></div>
                    
                    <div class="receipt-row">
                        <span>Amount:</span>
                        <span>₹{rate['initial_amount']}</span>
                    </div>
                    
                    <div class="receipt-row">
                        <span>Duration:</span>
                        <span>{rate['initial_duration']} hours</span>
                    </div>
                    
                    <div class="receipt-row">
                        <span>Mode:</span>
                        <span>{payment_mode}</span>
                    </div>
                    
                    <div class="receipt-divider"></div>
                    
                    <div class="receipt-row">
                        <span>Staff:</span>
                        <span>{handler_username}</span>
                    </div>
                </div>
                
                <div class="receipt-footer">
                    <p>Thank You!</p>
                    <small>Extra charges apply after {rate['initial_duration']} hours</small>
                    <small>(₹{rate['extra_charge']} per {rate['extra_charge_duration']} hours)</small>
                </div>
            </div>
        </div>
        '''
        
        return jsonify({
            'success': True,
            'message': f'Vehicle {vehicle_number} has been successfully checked in!',
            'receipt': receipt_html
        })
                            
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f'Error during check-in: {str(e)}'
        }) 