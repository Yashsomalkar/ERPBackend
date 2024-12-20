from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
   
    app.config["SECRET_KEY"] = "1337"

    
    # Initialize extensions
    mongo.init_app(app)
    print("MongoDB initialized:", mongo.cx)
    CORS(app)

    # Register blueprints
    from erp_app.routes.auth import auth_bp
    from erp_app.routes.user import user_bp
    from erp_app.routes.vendor import vendor_bp
    from erp_app.routes.admin import admin_bp
    from erp_app.routes.test import test_bp
    
    
    app.register_blueprint(test_bp, url_prefix="/api/test")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(vendor_bp, url_prefix="/api/vendor")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    return app
