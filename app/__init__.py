from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config
from app.utils.csrf import csrf

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    csrf.init_app(app)    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Import models
    from app.models.user import User
    from app.models.food_item import FoodItem
    from app.models.order import Order
    from app.models.payment import Payment
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes.auth import auth
    from app.routes.admin import admin
    from app.routes.customer import customer
    from app.routes.restaurant import restaurant
    from app.routes.main import main
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(customer, url_prefix='/customer')
    app.register_blueprint(restaurant, url_prefix='/restaurant')
    app.register_blueprint(main)
    
    return app


