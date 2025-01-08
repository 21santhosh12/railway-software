from flask import request, session, redirect, url_for, jsonify
from datetime import datetime
import math
from config import vehicles_collection, completed_records, rates_collection
from routes.calculate_charge import calculate_charge

def checkout():
    if 'username' not in session:
        return redirect(url_for('route_login'))
    
    try:
        vehicle_number = request.form.get('vehicle_number', '').upper()
        payment_mode = request.form.get('payment_mode')
        handler_username = session['username']
        
        # Find the vehicle check-in record for THIS user
        vehicle = vehicles_collection.find_one({
            'vehicle_number': vehicle_number,
            'handled_by': handler_username,
            'checkout_time': None
        })
        
        if not vehicle:
            # If not found under current user, check if it exists under another user
            other_vehicle = vehicles_collection.find_one({
                'vehicle_number': vehicle_number,
                'checkout_time': None
            })
            
            if other_vehicle:
                return jsonify({
                    'error': True,
                    'message': f'Vehicle {vehicle_number} was checked in by {other_vehicle["handled_by"]}. Only they can check it out.'
                })
            else:
                return jsonify({
                    'error': True,
                    'message': f'No active check-in found for vehicle {vehicle_number}!'
                })
        
        # Get the rate used during check-in
        rate = rates_collection.find_one({'_id': vehicle['rate_id']})
        if not rate:
            return jsonify({
                'error': True,
                'message': 'Rate configuration not found!'
            })
        
        checkout_time = datetime.now()
        elapsed_time = checkout_time - vehicle['checkin_time']
        hours = elapsed_time.total_seconds() / 3600
        
        # Calculate charges using stored rate
        total_charge = rate['initial_amount']
        additional_charge = 0
        
        if hours > rate['initial_duration']:
            extra_hours = hours - rate['initial_duration']
            extra_periods = math.ceil(extra_hours / rate['extra_charge_duration'])
            additional_charge = extra_periods * rate['extra_charge']
            total_charge += additional_charge
        
        # If additional payment is needed and we don't have payment mode yet
        if additional_charge > 0 and not payment_mode:
            return jsonify({
                'needsAdditionalPayment': True,
                'vehicle_number': vehicle_number,
                'checkin_time': vehicle['checkin_time'].strftime('%Y-%m-%d %H:%M:%S'),
                'checkout_time': checkout_time.strftime('%Y-%m-%d %H:%M:%S'),
                'initial_payment': rate['initial_amount'],
                'additional_charge': additional_charge,
                'total_charge': total_charge
            })
        
        # Process checkout with existing record format
        completed_record = {
            'vehicle_number': vehicle['vehicle_number'],
            'checkin_time': vehicle['checkin_time'],
            'checkout_time': checkout_time,
            'initial_payment': rate['initial_amount'],
            'additional_charge': additional_charge,
            'total_charge': total_charge,
            'initial_payment_mode': vehicle.get('payment_mode', 'N/A'),
            'additional_payment_mode': payment_mode if additional_charge > 0 else None,
            'handled_by': vehicle.get('handled_by', session['username']),
            'checkout_by': session['username']
        }
        
        # Insert into completed_records and delete from vehicles_collection
        completed_records.insert_one(completed_record)
        vehicles_collection.delete_one({'_id': vehicle['_id']})
        
        # Use existing receipt format with dynamic values
        receipt_html = f'''
        <div class="receipt-container" id="checkoutReceipt">
            <div class="receipt">
                <div class="receipt-header">
                    <h2>PARKING RECEIPT</h2>
                    <div class="receipt-divider"></div>
                </div>
                
                <div class="receipt-body">
                    <div class="receipt-row">
                        <span>Vehicle:</span>
                        <span>{vehicle_number}</span>
                    </div>
                    
                    <div class="receipt-row">
                        <span>Duration:</span>
                        <span>{vehicle['checkin_time'].strftime('%H:%M %d/%m')} - {checkout_time.strftime('%H:%M %d/%m')}</span>
                    </div>
                    
                    <div class="receipt-divider"></div>
                    
                    <div class="receipt-row">
                        <span>Initial:</span>
                        <span>₹{rate['initial_amount']} ({vehicle.get('payment_mode', 'N/A')})</span>
                    </div>
                    
                    {f"""
                    <div class="receipt-row">
                        <span>Add.Chrg:</span>
                        <span>₹{additional_charge} ({payment_mode})</span>
                    </div>
                    """ if additional_charge > 0 else ""}
                    
                    <div class="receipt-row total">
                        <span>TOTAL:</span>
                        <span>₹{total_charge}</span>
                    </div>
                    
                    <div class="receipt-divider"></div>
                    
                    <div class="receipt-row">
                        <span>Staff:</span>
                        <span>{session['username']}</span>
                    </div>
                </div>
                
                <div class="receipt-footer">
                    <p>Thank You!</p>
                </div>
            </div>
        </div>
        '''
        
        return jsonify({
            'success': True,
            'message': f'Vehicle {vehicle_number} has been successfully checked out!',
            'receipt': receipt_html
        })
                            
    except Exception as e:
        print(f"Error during check-out: {str(e)}")  # Debug print
        return jsonify({
            'error': True,
            'message': f'Error during check-out: {str(e)}'
        }) 