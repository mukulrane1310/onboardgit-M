from datetime import datetime, timezone
from uuid import uuid4

from app.db.collections import projects_collection


def create_project(repo_url: str, user_id: str):
    project = {
        "id": str(uuid4()),
       "user_id": user_id,
        "repo_url": repo_url,
        "repo_name": None,
        "default_branch": None,
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    projects_collection.insert_one(project)

    return project


def find_project_by_id(project_id: str):
    return projects_collection.find_one({"id": project_id})


def get_all_projects():
    return list(
        projects_collection.find(
            {},
            {"_id": 0},
        ).sort("created_at", -1)
    )


def update_project_status(project_id: str, status: str):
    projects_collection.update_one(
        {"id": project_id},
        {"$set": {"status": status}},
    )


def delete_project(project_id: str):
    result = projects_collection.delete_one({"id": project_id})
    return result.deleted_count > 0