from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.Enum('admin', 'customer', 'restaurant', name='user_roles'), default='customer')
    status = db.Column(db.Enum('active', 'pending', 'suspended', name='account_status'), default='active')

    food_items = db.relationship('FoodItem', backref='restaurant_owner', lazy=True, foreign_keys='FoodItem.restaurant_id')
    orders_as_customer = db.relationship('Order', backref='customer_user', lazy=True, foreign_keys='Order.customer_id')
    orders_as_restaurant = db.relationship('Order', backref='restaurant_user', lazy=True, foreign_keys='Order.restaurant_id')
    payments_as_customer = db.relationship('Payment', backref='customer_payer', lazy=True, foreign_keys='Payment.customer_id')
    payments_as_restaurant = db.relationship('Payment', backref='restaurant_receiver', lazy=True, foreign_keys='Payment.restaurant_id')

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.role}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

