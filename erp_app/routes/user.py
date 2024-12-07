from flask import Blueprint, jsonify, request
from ERPBackend.erp_app.utils.serializer import serialize_mongo_document
from erp_app.services.user_service import UserService
from erp_app.services.product_service import ProductService
from erp_app.services.cart_service import CartService
from erp_app.services.order_service import OrderService
from erp_app.utils.auth import user_required
user_bp = Blueprint("user", __name__)

@user_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = UserService.get_user_by_id(user_id)
        return jsonify(user), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@user_bp.route("/register", methods=["POST"])
def register_user():
    data = request.json
    try:
        UserService.create_user(data)
        return jsonify({"message": "User registered successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Public endpoints (no auth required)
@user_bp.route("/products", methods=["GET"])
def list_products():
    # Optional filters: vendor_id, name
    vendor_id = request.args.get("vendor_id")
    name = request.args.get("name")
    products = ProductService.get_products(vendor_id=vendor_id, name=name)
    return jsonify(products), 200

@user_bp.route("/products/<product_id>", methods=["GET"])
def get_product(product_id):
    product = ProductService.get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200

# Cart (user only)
@user_bp.route("/cart", methods=["POST"])
@user_required
def add_to_cart():
    data = request.json
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not product_id:
        return jsonify({"error": "product_id is required"}), 400

    CartService.add_to_cart(request.user_id, product_id, quantity)
    return jsonify({"message": "Product added to cart"}), 201

@user_bp.route("/cart", methods=["GET"])
@user_required
def view_cart():
    cart_items = CartService.get_cart(request.user_id)
    return jsonify(cart_items), 200

@user_bp.route("/cart/<product_id>", methods=["DELETE"])
@user_required
def remove_from_cart(product_id):
    CartService.remove_from_cart(request.user_id, product_id)
    return jsonify({"message": "Product removed from cart"}), 200

# Orders (user only)
@user_bp.route("/orders", methods=["POST"])
@user_required
def create_order():
    # Create an order from user's cart
    try:
        order = OrderService.create_order_from_cart(request.user_id)
        order = serialize_mongo_document(order)
        return jsonify(order), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route("/orders", methods=["GET"])
@user_required
def list_user_orders():
    orders = OrderService.get_orders_by_user(request.user_id)
    orders = serialize_mongo_document(orders)
    return jsonify(orders), 200

@user_bp.route("/orders/<order_id>", methods=["GET"])
@user_required
def get_user_order(order_id):
    order = OrderService.get_order_by_id(order_id)
    if not order or str(order["user_id"]) != request.user_id:
        return jsonify({"error": "Order not found or unauthorized"}), 404
    order = serialize_mongo_document(order)
    return jsonify(order), 200

@user_bp.route("/orders/<order_id>/cancel", methods=["PUT"])
@user_required
def cancel_order(order_id):
    try:
        updated_order = OrderService.update_order_status(request.user_id, order_id, "cancelled")
        updated_order = serialize_mongo_document(updated_order)
        return jsonify(updated_order), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400