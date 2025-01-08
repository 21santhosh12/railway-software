from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB Configuration
MONGO_URI = 'mongodb+srv://santhosh:2002Sk@parkingtokensystem.o4l8l.mongodb.net/?retryWrites=true&w=majority&ssl=true&authSource=admin&appName=ParkingTokenSystem'

# Create a MongoClient instance
client = MongoClient(MONGO_URI)

# Access the database and collections
db = client.ParkingTokenSystem
admins_collection = db.admins
users_collection = db.users
rates_collection = db.rates
vehicles_collection = db.vehicles
completed_records = db.completed_records

# Application Configuration
SECRET_KEY = 'Santhosh@2002'
MASTER_KEY = os.getenv('MASTER_KEY')

# Global variables
default_user_setup_done = False 