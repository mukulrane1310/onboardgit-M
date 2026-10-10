import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongodb_url = os.getenv("MONGODB_URL")

if not mongodb_url:
    raise RuntimeError("MONGODB_URL not found in .env")

client = MongoClient(mongodb_url)

client.admin.command("ping")

print("MongoDB connection successful!")