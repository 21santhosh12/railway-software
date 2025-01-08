import math

def calculate_charge(checkin_time, checkout_time, user):
    elapsed_time = checkout_time - checkin_time
    hours = elapsed_time.total_seconds() / 3600
    
    # Initial period charge
    charge = user['initial_amount']
    
    # If time exceeds initial duration, calculate extra charges
    if hours > user['initial_duration']:
        extra_hours = hours - user['initial_duration']
        extra_periods = math.ceil(extra_hours / user['extra_charge_duration'])
        charge += extra_periods * user['extra_charge']
    
    return charge 