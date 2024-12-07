import jwt
from functools import wraps
from flask import request, jsonify, current_app
from datetime import datetime, timedelta

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

def decode_token(token):
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
# erp_app/utils/auth.py


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Token missing"}), 401

        # If the header starts with "Bearer ", split it out
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
        else:
            token = auth_header

        try:
            payload = jwt.decode(token, "1337", algorithms=["HS256"])
            print("Decoded JWT Payload:", payload)  # Debugging: Print the entire payload
            print("Extracted user_id from JWT:", payload["user_id"])  # Debugging: Print user_id
            request.user_id = payload["user_id"]
            request.user_role = payload["role"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if request.user_role != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated

def vendor_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if request.user_role != "vendor":
            return jsonify({"error": "Vendor access required"}), 403
        return f(*args, **kwargs)
    return decorated

def user_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if request.user_role != "user":
            return jsonify({"error": "User access required"}), 403
        return f(*args, **kwargs)
    return decorated