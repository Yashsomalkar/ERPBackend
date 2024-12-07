from bson import ObjectId
from erp_app.models.cart import CartModel
from erp_app.models.product import ProductModel  # to validate product existence if needed
from datetime import datetime

class CartService:
    @staticmethod
    def add_to_cart(user_id, product_id, quantity=1):
        # Validate product existence (optional but recommended)
        product = ProductModel.find_product_by_id(ObjectId(product_id))
        if not product:
            raise ValueError("Product does not exist")

        cart = CartModel.find_cart_by_user_id(ObjectId(user_id))
        if not cart:
            # Create a new cart if it doesn't exist
            cart_id = CartModel.create_cart(ObjectId(user_id))
            cart = CartModel.find_cart_by_user_id(ObjectId(user_id))

        # Check if the product is already in the cart
        items = cart.get("items", [])
        for item in items:
            if item["product_id"] == ObjectId(product_id):
                # Increase the quantity
                item["quantity"] += quantity
                break
        else:
            # Add a new item if not found
            items.append({
                "product_id": ObjectId(product_id),
                "quantity": quantity
            })

        # Update cart
        CartModel.update_cart_items(ObjectId(user_id), items)

    @staticmethod
    def get_cart(user_id):
        cart = CartModel.find_cart_by_user_id(ObjectId(user_id))
        if not cart:
            return {"items": []}
        
        # Optionally, you could enrich items with product details
        # For simplicity, we just return the items as is
        return {"items": cart.get("items", [])}

    @staticmethod
    def remove_from_cart(user_id, product_id):
        cart = CartModel.find_cart_by_user_id(ObjectId(user_id))
        if not cart or "items" not in cart:
            return
        
        items = cart["items"]
        updated_items = [item for item in items if item["product_id"] != ObjectId(product_id)]

        # Update cart if there is a change
        if len(updated_items) != len(items):
            CartModel.update_cart_items(ObjectId(user_id), updated_items)
