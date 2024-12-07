from datetime import datetime
from bson import ObjectId
from erp_app import mongo

class CartModel:
    @staticmethod
    def find_cart_by_user_id(user_id):
        return mongo.db.carts.find_one({"user_id": user_id})

    @staticmethod
    def create_cart(user_id):
        data = {
            "user_id": user_id,
            "items": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        return mongo.db.carts.insert_one(data).inserted_id

    @staticmethod
    def update_cart_items(user_id, items):
        return mongo.db.carts.update_one(
            {"user_id": user_id},
            {"$set": {"items": items, "updated_at": datetime.utcnow()}}
        )

    @staticmethod
    def remove_item(user_id, product_id):
        # If you decide to implement a direct remove method, you can do:
        return mongo.db.carts.update_one(
            {"user_id": user_id},
            {"$pull": {"items": {"product_id": product_id}}}
        )

    @staticmethod
    def clear_cart_by_user_id(user_id):
        return mongo.db.carts.update_one({"user_id": user_id}, {"$set": {"items": []}})