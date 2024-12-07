from erp_app.models.vendor import VendorModel

class VendorService:
    @staticmethod
    def create_vendor(data):
        """
        Validates and creates a new vendor.
        """
        if not data.get("business_name"):
            raise ValueError("Business name is required")

        return VendorModel.create_vendor(data)

    @staticmethod
    def get_vendor_by_user_id(user_id):
        vendor = VendorModel.find_vendor_by_user_id(user_id)
        if not vendor:
            raise ValueError("Vendor not found")
        return vendor

    @staticmethod
    def update_vendor(vendor_id, data):
        """
        Updates an existing vendor's details.
        """
        return VendorModel.update_vendor(vendor_id, data)
