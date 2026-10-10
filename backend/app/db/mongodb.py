import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_DB = os.getenv("MONGODB_DB", "onboardgit")

if not MONGODB_URL:
    raise RuntimeError("MONGODB_URL not found in .env")


client = MongoClient(MONGODB_URL)
db = client[MONGODB_DB]


def get_database():
    return db