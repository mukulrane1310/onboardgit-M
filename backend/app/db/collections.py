from app.db.mongodb import get_database


db = get_database()

users_collection = db["users"]
projects_collection = db["projects"]
analysis_reports_collection = db["analysis_reports"]
file_hotspots_collection = db["file_hotspots"]
file_ownership_collection = db["file_ownership"]
temporal_coupling_collection = db["temporal_coupling"]