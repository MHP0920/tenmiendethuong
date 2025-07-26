from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from config import settings

class Database:
    client = None
    database = None

db = Database()

async def connect_to_mongo():
    """Create database connection"""
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db.database = db.client[settings.DATABASE_NAME]
    print(f"Connected to MongoDB at {settings.MONGODB_URL}")

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB")

def get_database():
    """Get database instance"""
    return db.database

# Collections
def get_users_collection():
    return db.database.users

def get_sessions_collection():
    return db.database.game_sessions

def get_payments_collection():
    return db.database.payments
