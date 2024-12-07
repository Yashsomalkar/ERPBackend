from flask import Blueprint, jsonify
from erp_app import mongo

test_bp = Blueprint("test", __name__)

@test_bp.route("/test-db", methods=["GET"])
def test_db():
    # Insert a sample document
    mongo.db.test.insert_one({"message": "Hello, MongoDB!"})
    # Retrieve the document
    document = mongo.db.test.find_one({"message": "Hello, MongoDB!"})
    return jsonify({"message": document["message"]})
