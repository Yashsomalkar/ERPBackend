from datetime import datetime
from erp_app import mongo

class OrderModel:
    @staticmethod
    def create_order(data):
        """
        Creates a new order with timestamps.
        """
        data["status"] = "pending"  # Default status
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        return mongo.db.orders.insert_one(data)

    @staticmethod
    def find_order_by_id(order_id):
        """
        Finds an order by its ID.
        """
        return mongo.db.orders.find_one({"_id": order_id})

    @staticmethod
    def update_order_status(order_id, status):
        """
        Updates the status of an order.
        """
        return mongo.db.orders.update_one(
            {"_id": order_id},
            {"$set": {"status": status, "updated_at": datetime.utcnow()}}
        )
