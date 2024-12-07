from flask import Blueprint, request, jsonify
from erp_app.utils.auth import vendor_required
from erp_app.services.vendor_service import VendorService
from erp_app.services.product_service import ProductService
from erp_app.services.order_service import OrderService
from erp_app.utils.serializer import serialize_mongo_document
vendor_bp = Blueprint("vendor", __name__)





@vendor_bp.route("/me", methods=["GET"])
@vendor_required
def get_vendor_info():
    try:
        vendor = VendorService.get_vendor_by_user_id(request.user_id)
        if not vendor:
            return jsonify({"error": "Vendor not found"}), 404
        
        # Use utility function to serialize the document
        serialized_vendor = serialize_mongo_document(vendor)

        return jsonify(serialized_vendor), 200
    except ValueError:
        return jsonify({"error": "Vendor not found"}), 404




@vendor_bp.route("/me", methods=["PUT"])
@vendor_required
def update_vendor_info():
    # Updates vendor details such as address, phone, etc.
    data = request.json
    updated_vendor = VendorService.update_vendor(request.user_id, data)
    serialized_updated_vendor = serialize_mongo_document(updated_vendor)
    if not updated_vendor:
        return jsonify({"error": "Vendor not found or update failed"}), 404
    return jsonify(serialized_updated_vendor), 200

@vendor_bp.route("/products", methods=["POST"])
@vendor_required
def add_product():
    # Adds a new product under the vendor's catalog
    data = request.json
    try:
        product = ProductService.create_product_for_vendor(request.user_id, data)
        serialized_product = serialize_mongo_document(product)
        return jsonify(serialized_product), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@vendor_bp.route("/products", methods=["GET"])
@vendor_required
def get_own_products():
    # Lists all products owned by the vendor
    try:
        products = ProductService.get_products_by_vendor(request.user_id)
        serialized_products = serialize_mongo_document(products)
        return jsonify(serialized_products), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@vendor_bp.route("/products/<product_id>", methods=["PUT"])
@vendor_required
def update_product(product_id):
    # Updates details of a specific product owned by the vendor
    data = request.json
    updated = ProductService.update_vendor_product(request.user_id, product_id, data)
    serialized_updated = serialize_mongo_document(updated)
    if not updated:
        return jsonify({"error": "Product not found or unauthorized"}), 404
    return jsonify(serialized_updated), 200

@vendor_bp.route("/products/<product_id>", methods=["DELETE"])
@vendor_required
def delete_product(product_id):
    # Deletes a specific product owned by the vendor
    success = ProductService.delete_vendor_product(request.user_id, product_id)
    if not success:
        return jsonify({"error": "Product not found or unauthorized"}), 404
    return jsonify({"message": "Product deleted"}), 200

@vendor_bp.route("/orders", methods=["GET"])
@vendor_required
def get_vendor_orders():
    # Lists orders that include the vendor's products
    orders = OrderService.get_orders_for_vendor(request.user_id)
    serialized_orders = serialize_mongo_document(orders)
    return jsonify(serialized_orders), 200

@vendor_bp.route("/orders/<order_id>/fulfill", methods=["PUT"])
@vendor_required
def fulfill_order(order_id):
    # Fulfill (complete) an order that includes the vendor's products
    try:
        fulfilled_order = OrderService.fulfill_vendor_order(request.user_id, order_id)
        serialized_fulfilled_order = serialize_mongo_document(fulfilled_order)
        return jsonify(serialized_fulfilled_order), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
