from datetime import datetime
from bson import ObjectId
#from bson import ObjectId
from erp_app import mongo

class VendorModel:
    @staticmethod
    def create_vendor(data):
        """
        Creates a new vendor with timestamps.
        """
        data["products"] = []  # Initialize an empty products list
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        return mongo.db.vendors.insert_one(data)



class VendorModel:
    @staticmethod
    def find_vendor_by_user_id(user_id):
        """
        Finds a vendor by the associated user ID.
        """
        try:
            # Ensure user_id is an ObjectId
            if not isinstance(user_id, ObjectId):
                user_id = ObjectId(user_id)
            
            print(f"Querying vendors collection with user_id: {user_id}")  # Debugging
            vendor = mongo.db.vendors.find_one({"user_id": user_id})
            
            if not vendor:
                print("No vendor found for this user_id")
            
            return vendor
        except Exception as e:
            print(f"Error querying vendor: {e}")
            raise




    @staticmethod
    def update_vendor(vendor_id, data):
        """
        Updates a vendor's details with timestamps.
        """
        data["updated_at"] = datetime.utcnow()
        return mongo.db.vendors.update_one({"_id": vendor_id}, {"$set": data})
    @staticmethod
    def get_all_vendors():
        return mongo.db.vendors.find({})