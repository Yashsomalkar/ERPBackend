from datetime import datetime
from bson import ObjectId
from ERPBackend.erp_app.models.cart import CartModel
from erp_app.models.order import OrderModel
from erp_app.models.product import ProductModel

class OrderService:
    @staticmethod
    def create_order(user_id, product_ids):
        """
        Creates a new order for a user.
        """
        # Check if products exist
        products = [ProductModel.find_product_by_id(product_id) for product_id in product_ids]
        if not all(products):
            raise ValueError("One or more products do not exist")

        # Calculate total amount
        total_amount = sum(product["price"] for product in products)

        # Create order
        order_data = {
            "user_id": user_id,
            "product_ids": product_ids,
            "total_amount": total_amount,
            "status": "pending"
        }
        return OrderModel.create_order(order_data)

    @staticmethod
    def get_order_by_id(order_id):
        """
        Retrieves an order by its ID.
        """
        order = OrderModel.find_order_by_id(order_id)
        if not order:
            raise ValueError("Order not found")
        return order

    @staticmethod
    def update_order_status(order_id, status):
        """
        Updates the status of an order.
        """
        valid_statuses = ["pending", "completed", "cancelled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Choose from {valid_statuses}")
        return OrderModel.update_order_status(order_id, status)
   
    @staticmethod
    def create_order_from_cart(user_id):
        """
        Creates an order for a user based on their cart.
        - Fetch cart items for the user.
        - Validate product availability.
        - Calculate total amount.
        - Deduct quantities from products.
        - Create an order in the database.
        - Clear the user's cart.
        """
        # Step 1: Fetch the user's cart
        cart = CartModel.find_cart_by_user_id(ObjectId(user_id))
        if not cart or not cart.get("items"):
            raise ValueError("Cart is empty")

        items = cart["items"]  # List of {product_id, quantity}
        total_amount = 0
        order_items = []

        # Step 2: Validate product availability and calculate total
        for item in items:
            product_id = ObjectId(item["product_id"])
            quantity = item["quantity"]

            product = ProductModel.find_product_by_id(product_id)
            if not product:
                raise ValueError(f"Product with ID {product_id} not found")
            
            if product["quantity"] < quantity:
                raise ValueError(f"Insufficient stock for product: {product['name']}")

            # Update total amount and prepare order items
            total_amount += product["price"] * quantity
            order_items.append({
                "product_id": product["_id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity
            })

        # Step 3: Deduct product quantities
        for item in items:
            product_id = ObjectId(item["product_id"])
            quantity = item["quantity"]

            ProductModel.update_product(product_id, {
                "quantity": ProductModel.find_product_by_id(product_id)["quantity"] - quantity
            })

        # Step 4: Create the order
        order_data = {
            "user_id": ObjectId(user_id),
            "items": order_items,
            "total_amount": total_amount,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        result = OrderModel.create_order(order_data)

        # Step 5: Clear the user's cart
        CartModel.clear_cart_by_user_id(ObjectId(user_id))

        # Step 6: Return the created order
        return OrderModel.find_order_by_id(result.inserted_id)