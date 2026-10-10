from uuid import uuid4

from app.db.collections import users_collection


def find_user_by_email(email: str):
    return users_collection.find_one({"email": email})


def find_user_by_id(user_id: str):
    return users_collection.find_one({"id": user_id})


def create_user(username: str, email: str, hashed_password: str):
    user = {
        "id": str(uuid4()),
        "username": username,
        "email": email,
        "hashed_password": hashed_password,
    }

    users_collection.insert_one(user)

    return user