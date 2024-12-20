
from datetime import datetime
from bson import ObjectId
from flask import Blueprint, request, jsonify
from erp_app.models.user import UserModel
from erp_app.models.vendor import VendorModel
from erp_app.utils.auth import admin_required
from erp_app.utils.serializer import serialize_mongo_document
admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/users", methods=["GET"])
@admin_required
def get_all_users():
    users = list(UserModel.get_all_users())
    users = serialize_mongo_document(users)
    return jsonify(users), 200

@admin_bp.route("/vendors", methods=["GET"])
@admin_required
def get_all_vendors():
    vendors = list(VendorModel.get_all_vendors())
    vendors = serialize_mongo_document(vendors)
    return jsonify(vendors), 200


# Add a new user
@admin_bp.route("/users", methods=["POST"])
@admin_required
def add_user():
    data = request.json

    # Validate input
    if not data.get("name") or not data.get("email") or not data.get("membership"):
        return jsonify({"error": "Name, email, and membership are required"}), 400

    try:
        # Check if the email is already registered
        if UserModel.find_user_by_email(data["email"]):
            return jsonify({"error": "User with this email already exists"}), 400

        # Create the user
        new_user = {
            "name": data["name"],
            "email": data["email"],
            "membership": data["membership"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        UserModel.create_user(new_user)
        return jsonify({"message": "User added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update an existing user
@admin_bp.route("/users/<user_id>", methods=["PUT"])
@admin_required
def update_user(user_id):
    data = request.json

    # Validate input
    if not data.get("name") or not data.get("email") or not data.get("membership"):
        return jsonify({"error": "Name, email, and membership are required"}), 400

    try:
        # Update user data
        updated_user = {
            "name": data["name"],
            "email": data["email"],
            "membership": data["membership"],
            "updated_at": datetime.utcnow(),
        }

        result = UserModel.update_user(ObjectId(user_id), updated_user)
        if result.modified_count == 0:
            return jsonify({"error": "User not found or no changes made"}), 404

        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a user
@admin_bp.route("/users/<user_id>", methods=["DELETE"])
@admin_required
def delete_user(user_id):
    try:
        result = UserModel.delete_user(ObjectId(user_id))
        if result.deleted_count == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500