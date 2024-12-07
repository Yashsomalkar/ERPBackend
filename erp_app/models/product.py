from datetime import datetime
from erp_app import mongo

class ProductModel:
    @staticmethod
    def create_product(data):
        """
        Creates a new product with timestamps.
        """
        data["status"] = "available"  # Default status
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        return mongo.db.products.insert_one(data)

    @staticmethod
    def find_product_by_id(product_id):
        """
        Finds a product by its ID.
        """
        return mongo.db.products.find_one({"_id": product_id})

    @staticmethod
    def update_product(product_id, data):
        """
        Updates a product's details with timestamps.
        """
        data["updated_at"] = datetime.utcnow()
        return mongo.db.products.update_one({"_id": product_id}, {"$set": data})
    @staticmethod
    def find_products(query):
        return mongo.db.products.find(query)


    @staticmethod
    def delete_product(product_id):
        return mongo.db.products.delete_one({"_id": product_id})