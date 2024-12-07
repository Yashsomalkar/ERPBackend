from erp_app.models.user import UserModel

class UserService:
    @staticmethod
    def create_user(data):
        """
        Validates and creates a new user.
        """
        if not data.get("email") or not data.get("password"):
            raise ValueError("Email and password are required")

        if UserModel.find_user_by_email(data["email"]):
            raise ValueError("User already exists")

        return UserModel.create_user(data)

    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieves a user by their ID.
        """
        user = UserModel.find_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    @staticmethod
    def update_user(user_id, data):
        """
        Updates an existing user's details.
        """
        return UserModel.update_user(user_id, data)
