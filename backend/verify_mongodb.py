import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

mongodb_url = os.getenv("MONGODB_URL")
mongodb_db = os.getenv("MONGODB_DB", "onboardgit")

if not mongodb_url:
    raise RuntimeError("MONGODB_URL not found in .env")


client = MongoClient(mongodb_url)
db = client[mongodb_db]

collections = [
    "users",
    "projects",
    "analysis_reports",
    "file_hotspots",
    "file_ownership",
    "temporal_coupling",
]


print(f"Database: {mongodb_db}")
print()

for collection_name in collections:
    count = db[collection_name].count_documents({})
    print(f"{collection_name}: {count} records")

print()
print("MongoDB verification completed!")

client.close()