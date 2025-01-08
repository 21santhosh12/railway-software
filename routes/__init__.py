# This file makes the routes directory a Python package

from .admin_dashboard import admin_dashboard
from .admin_register import admin_register
from .calculate_charge import calculate_charge
from .checkin import checkin
from .checkout import checkout
from .create_user import create_user
from .delete_admin import delete_admin
from .delete_user import delete_user
from .generate_admin_code import generate_admin_code
from .generate_report import generate_report
from .get_vehicle_suggestions import get_vehicle_suggestions
from .handle_vehicle import handle_vehicle
from .home import home
from .index import index
from .login import login
from .logout import logout
from .register import register
from .setup_default_user import setup_default_user
from .update_existing_admins import update_existing_admins

__all__ = [
    'admin_dashboard',
    'admin_register',
    'calculate_charge',
    'checkin',
    'checkout',
    'create_user',
    'delete_admin',
    'delete_user',
    'generate_admin_code',
    'generate_report',
    'get_vehicle_suggestions',
    'handle_vehicle',
    'home',
    'index',
    'login',
    'logout',
    'register',
    'setup_default_user',
    'update_existing_admins'
] 