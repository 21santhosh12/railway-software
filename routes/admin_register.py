from flask import render_template, request, flash, redirect, url_for, session
from datetime import datetime
from config import admins_collection
import logging
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_APP_PASSWORD = os.getenv('ADMIN_APP_PASSWORD')

def send_otp_email(otp):
    try:
        msg = MIMEMultipart()
        msg['From'] = ADMIN_EMAIL
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = "Admin Registration OTP Verification"
        
        body = f"Your OTP for admin registration is: {otp}"
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(ADMIN_EMAIL, ADMIN_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def admin_register():
    if request.method == 'POST':
        if 'verify_otp' in request.form:
            # OTP verification phase
            user_otp = request.form.get('otp')
            stored_otp = session.get('admin_registration_otp')
            username = session.get('temp_username')
            password = session.get('temp_password')
            
            if not stored_otp or not username or not password:
                flash('Session expired. Please try again', 'danger')
                return redirect(url_for('route_admin_register'))
            
            if user_otp == stored_otp:
                # Create new admin
                admin = {
                    'username': username,
                    'password': password,
                    'created_at': datetime.now(),
                    'is_admin': True
                }
                
                try:
                    result = admins_collection.insert_one(admin)
                    if result.inserted_id:
                        # Clear session data
                        session.pop('admin_registration_otp', None)
                        session.pop('temp_username', None)
                        session.pop('temp_password', None)
                        
                        flash('Admin account created successfully', 'success')
                        return redirect(url_for('route_login'))
                    else:
                        flash('Failed to create admin account', 'danger')
                except Exception as e:
                    flash(f'Error creating admin account: {str(e)}', 'danger')
            else:
                flash('Wrong OTP. Please contact administrator', 'danger')
                return render_template('admin_register.html', show_otp_form=True)
                
        else:
            # Initial registration phase
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            if password != confirm_password:
                flash('Passwords do not match', 'danger')
                return render_template('admin_register.html')

            existing_admin = admins_collection.find_one({'username': username})
            if existing_admin:
                flash('Username already exists', 'danger')
                return render_template('admin_register.html')

            # Generate OTP
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            
            # Store registration data in session
            session['admin_registration_otp'] = otp
            session['temp_username'] = username
            session['temp_password'] = password
            
            # Send OTP via email
            if send_otp_email(otp):
                flash('OTP has been sent to admin email', 'success')
                return render_template('admin_register.html', show_otp_form=True)
            else:
                flash('Failed to send OTP. Please try again', 'danger')
                return render_template('admin_register.html')

    return render_template('admin_register.html', show_otp_form=False) 