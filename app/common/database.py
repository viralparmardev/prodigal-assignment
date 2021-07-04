import pymongo
from .config import MONGDB_CONNECTION_STRING, DATABASE_NAME

client = pymongo.MongoClient(MONGDB_CONNECTION_STRING)
db = client[DATABASE_NAME]

