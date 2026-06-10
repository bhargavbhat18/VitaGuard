import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import sys
import os

# Add parent dir to path so we can import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.config import MONGO_URI, DB_NAME

async def migrate_roles():
    print(f"Connecting to MongoDB: {DB_NAME}")
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    # Update users missing a role to have PATIENT role
    result = await db.users.update_many(
        {"role": {"$exists": False}},
        {"$set": {"role": "PATIENT"}}
    )
    
    print(f"Migration completed. Modified {result.modified_count} users.")
    client.close()

if __name__ == "__main__":
    asyncio.run(migrate_roles())
