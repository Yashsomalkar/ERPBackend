from bson import ObjectId
from erp_app.models.product import ProductModel
from erp_app.models.vendor import VendorModel

class ProductService:
    @staticmethod
    def get_products(vendor_id=None, name=None):
        """
        Retrieve all products, with optional filters by vendor_id or product name.
        """
        query = {}
        if vendor_id:
            # Ensure vendor_id is an ObjectId before querying
            query["vendor_id"] = ObjectId(vendor_id)
        if name:
            # Use case-insensitive regex search if desired
            query["name"] = {"$regex": name, "$options": "i"}
        
        return list(ProductModel.find_products(query))

    @staticmethod
    def get_product_by_id(product_id):
        """
        Retrieve a single product by its ID.
        """
        if not ObjectId.is_valid(product_id):
            return None
        return ProductModel.find_product_by_id(ObjectId(product_id))

    @staticmethod
    def create_product_for_vendor(user_id, data):
        """
        Create a new product linked to the vendor associated with user_id.
        - First find the vendor using user_id.
        - Then create a product under that vendor.
        """
        vendor = VendorModel.find_vendor_by_user_id(ObjectId(user_id))
        if not vendor:
            raise ValueError("Vendor not found for this user")

        # Validate required product fields
        if not data.get("name") or not data.get("price") or not data.get("quantity"):
            raise ValueError("Product name, price, and quantity are required")

        product_data = {
            "vendor_id": vendor["_id"],
            "name": data["name"],
            "description": data.get("description", ""),
            "price": float(data["price"]),
            "quantity": int(data["quantity"]),
            "status": data.get("status", "available"),
        }
        result = ProductModel.create_product(product_data)
        return ProductModel.find_product_by_id(result.inserted_id)

    @staticmethod
    def get_products_by_vendor(user_id):
        """
        Retrieve all products for the vendor associated with user_id.
        """
        vendor = VendorModel.find_vendor_by_user_id(ObjectId(user_id))
        if not vendor:
            raise ValueError("Vendor not found for this user")

        query = {"vendor_id": vendor["_id"]}
        return list(ProductModel.find_products(query))

    @staticmethod
    def update_vendor_product(user_id, product_id, data):
        """
        Update a product if it belongs to the vendor associated with user_id.
        - Check if the product exists and that it belongs to the vendor.
        - Only then update it.
        """
        # Debugging: Log product_id and user_id
        print(f"Attempting to update product: {product_id} by vendor user: {user_id}")

        # Step 1: Check if the product exists
        product = ProductModel.find_product_by_id(ObjectId(product_id))
        if not product:
            print(f"Product not found: {product_id}")
            return None

        # Debugging: Log the retrieved product
        print(f"Product found: {product}")

        # Step 2: Find the vendor by user_id
        vendor = VendorModel.find_vendor_by_user_id(ObjectId(user_id))
        if not vendor:
            print(f"Vendor not found for user: {user_id}")
            return None

        # Debugging: Log the retrieved vendor
        print(f"Vendor found: {vendor}")

        # Step 3: Check if the product belongs to the vendor
        if product["vendor_id"] != vendor["_id"]:
            print(f"Unauthorized update attempt. Product's vendor_id: {product['vendor_id']} does not match vendor's _id: {vendor['_id']}")
            return None

        # Debugging: Log update_data
        update_data = {}
        if "name" in data:
            update_data["name"] = data["name"]
        if "description" in data:
            update_data["description"] = data["description"]
        if "price" in data:
            update_data["price"] = float(data["price"])
        if "quantity" in data:
            update_data["quantity"] = int(data["quantity"])
        if "status" in data:
            update_data["status"] = data["status"]

        if update_data:
            print(f"Updating product with data: {update_data}")
            ProductModel.update_product(ObjectId(product_id), update_data)
            return ProductModel.find_product_by_id(ObjectId(product_id))

        print(f"No updates made to product: {product_id}")
        return product


    @staticmethod
    def delete_vendor_product(user_id, product_id):
        """
        Delete a product if it belongs to the vendor associated with user_id.
        """
        product = ProductModel.find_product_by_id(ObjectId(product_id))
        if not product:
            return False

        vendor = VendorModel.find_vendor_by_user_id(ObjectId(user_id))
        if not vendor or product["vendor_id"] != vendor["_id"]:
            return False  # Unauthorized

        ProductModel.delete_product(ObjectId(product_id))
        return True
