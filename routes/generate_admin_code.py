import random
import string

def generate_admin_code():
    # Generate a 6-digit code
    return ''.join(random.choices(string.digits, k=6)) 