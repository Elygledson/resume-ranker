from config.settings import settings
from motor.motor_asyncio import AsyncIOMotorClient


def get_mongo_collection(collection_name: str):
    client = AsyncIOMotorClient(settings.database_url)
    db = client[settings.MONGO_INITDB_ROOT_DBNAME]
    return db.get_collection(collection_name)
