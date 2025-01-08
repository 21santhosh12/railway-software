from datetime import datetime
from config import users_collection

def update_existing_admins():
    users_collection.update_many(
        {'created_at': {'$exists': False}},
        {'$set': {'created_at': datetime.now()}}
    ) 