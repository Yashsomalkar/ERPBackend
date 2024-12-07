from flask import Blueprint, request, jsonify
import jwt
from erp_app.models.user import UserModel
from erp_app.models.vendor import VendorModel
from bson import ObjectId
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

SECRET_KEY = "1337"  # Replace with a secure key

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    # Validate input
    if not data.get("email") or not data.get("password") or not data.get("name"):
        return jsonify({"error": "Name, email, and password are required"}), 400

    role = data.get("role", "user")  # Default role is "user"

    # Check if user already exists
    if UserModel.find_user_by_email(data["email"]):
        return jsonify({"error": "User already exists"}), 400

    # Hash the password
    hashed_password = generate_password_hash(data["password"])

    # Create user data
    user = {
        "name": data["name"],
        "email": data["email"],
        "password": hashed_password,
        "role": role,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    # Insert user into the database and get the user ID
    user_id = UserModel.create_user(user).inserted_id

    # If the role is "vendor," add additional vendor details
    if role == "vendor":
        if not data.get("business_name") or not data.get("address") or not data.get("phone"):
            return jsonify({"error": "Business name, address, and phone are required for vendors"}), 400

        vendor = {
            "user_id": ObjectId(user_id),
            "business_name": data["business_name"],
            "address": data["address"],
            "phone": data["phone"],
            "products": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        VendorModel.create_vendor(vendor)

    return jsonify({"message": f"{role.capitalize()} registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    # Validate input
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required"}), 400

    # Fetch user from the database
    user = UserModel.find_user_by_email(data["email"])
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    # Verify the password
    if not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate JWT token
    payload = {
        "user_id": str(user["_id"]),
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token}), 200

@auth_bp.route("/register/admin", methods=["POST"])
def register_admin():
    data = request.json

    if not data.get("email") or not data.get("password") or not data.get("name"):
        return jsonify({"error": "Name, email, and password are required"}), 400

    # Admin role fixed here
    role = "admin"

    # Check if user already exists
    if UserModel.find_user_by_email(data["email"]):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(data["password"])

    user = {
        "name": data["name"],
        "email": data["email"],
        "password": hashed_password,
        "role": role,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    UserModel.create_user(user)

    return jsonify({"message": "Admin registered successfully"}), 201

@auth_bp.route("/login/admin", methods=["POST"])
def login_admin():
    data = request.json

    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required"}), 400

    user = UserModel.find_user_by_email(data["email"])
    if not user or user["role"] != "admin":
        return jsonify({"error": "Invalid credentials"}), 401

    if not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    payload = {
        "user_id": str(user["_id"]),
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token}), 200

@auth_bp.route("/login/vendor", methods=["POST"])
def login_vendor():
    data = request.json

    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required"}), 400

    user = UserModel.find_user_by_email(data["email"])
    if not user or user["role"] != "vendor":
        return jsonify({"error": "Invalid credentials"}), 401

    if not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    payload = {
        "user_id": str(user["_id"]),
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token}), 200
