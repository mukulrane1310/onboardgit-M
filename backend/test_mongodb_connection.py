from app.db.mongodb import get_database


db = get_database()

db.command("ping")

print("FastAPI MongoDB connection successful!")
print(f"Database: {db.name}")