from pymongo import MongoClient
from config.settings import settings


def get_mongo_collection(collection_name: str):
    client = MongoClient(settings.database_url)
    db = client[settings.MONGO_INITDB_ROOT_DBNAME]
    return db.get_collection(collection_name)
