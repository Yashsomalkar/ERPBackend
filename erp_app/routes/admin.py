
from flask import Blueprint, jsonify
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
