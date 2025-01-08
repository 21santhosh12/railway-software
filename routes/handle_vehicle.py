from flask import request, session, redirect, url_for, render_template
from datetime import datetime
from config import vehicles_collection, completed_records
from routes.calculate_charge import calculate_charge

def handle_vehicle():
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        vehicle_number = request.form['vehicle_number'].upper()
        action = request.form.get('action')
        payment_mode = request.form.get('payment_mode')

        if action == "checkin":
            # Check if the vehicle is already checked in
            existing_vehicle = vehicles_collection.find_one(
                {'vehicle_number': vehicle_number, 'checkout_time': None}
            )
            if existing_vehicle:
                return render_template('home.html', username=session['username'],
                                       error=f"Vehicle {vehicle_number} is already checked in!")

            # Perform check-in
            checkin_time = datetime.now()
            default_price = 15  # Default price for parking

            vehicle = {
                'vehicle_number': vehicle_number,
                'checkin_time': checkin_time,
                'checkout_time': None,
                'charge': None,
                'payment_mode': payment_mode,
                'handled_by': session['username']
            }
            vehicles_collection.insert_one(vehicle)

            # Show success message with Print button
            return render_template('home.html',
                                   username=session['username'],
                                   message=f"Vehicle {vehicle_number} checked in successfully!",
                                   print_required=True,
                                   vehicle_number=vehicle_number,
                                   checkin_time=checkin_time,
                                   price=default_price,
                                   payment_mode=payment_mode)

        elif action == "checkout":
            # Find the most recent check-in record without a checkout time
            vehicle = vehicles_collection.find_one(
                {'vehicle_number': vehicle_number, 'checkout_time': None},
                sort=[('checkin_time', -1)]  # Sort by most recent check-in
            )
            if not vehicle:
                return render_template('home.html', username=session['username'],
                                       error=f"No active check-in record found for vehicle {vehicle_number}!")

            # Perform check-out
            checkout_time = datetime.now()
            checkin_time = vehicle['checkin_time']
            charge = calculate_charge(checkin_time, checkout_time, vehicle)

            # Update the vehicle record with checkout details
            vehicles_collection.update_one(
                {'_id': vehicle['_id']},
                {'$set': {'checkout_time': checkout_time, 'charge': charge}}
            )

            # Move the completed record to the `completed_records` collection
            completed_records_collection = completed_records
            completed_record = vehicles_collection.find_one({'_id': vehicle['_id']})
            completed_records_collection.insert_one(completed_record)

            # Delete the record from the active `vehicles` collection
            vehicles_collection.delete_one({'_id': vehicle['_id']})

            # Show success message with Print button
            return render_template('home.html',
                                   username=session['username'],
                                   message=f"Vehicle {vehicle_number} checked out successfully!",
                                   print_required=True,
                                   vehicle_number=vehicle_number,
                                   checkin_time=checkin_time,
                                   checkout_time=checkout_time,
                                   charge=charge,
                                   payment_mode=vehicle.get('payment_mode', 'N/A'))

        else:
            return render_template('home.html', username=session['username'],
                                   error="Invalid action selected!")
    except Exception as e:
        return render_template('home.html', username=session['username'], error=f"Error: {str(e)}") 