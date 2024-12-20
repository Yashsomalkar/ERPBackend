from datetime import datetime
from werkzeug.security import generate_password_hash
from erp_app import mongo

class UserModel:
    @staticmethod
    def create_user(data):
        """
        Creates a new user with hashed password and timestamps.
        """
        data["password"] = data["password"]  # Hash the password
        data["role"] = data.get("role", "user")  # Default role to "user"
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        return mongo.db.users.insert_one(data)

    @staticmethod
    def find_user_by_email(email):
        """
        Finds a user by email.
        """
        return mongo.db.users.find_one({"email": email})

    @staticmethod
    def update_user(user_id, data):
        """
        Updates an existing user's details with timestamps.
        """
        data["updated_at"] = datetime.utcnow()
        return mongo.db.users.update_one({"_id": user_id}, {"$set": data})
    @staticmethod
    def get_all_users():
        return mongo.db.users.find({})
    @staticmethod
    def delete_user(user_id):
        return mongo.db.users.delete_one({"_id": user_id})