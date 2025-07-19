from app import db
from datetime import datetime

class FoodItem(db.Model):
    __tablename__ = 'food_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship('Order', backref='food_item', lazy=True)

    def __repr__(self):
        return f"FoodItem('{self.name}', '{self.price}', Restaurant ID: {self.restaurant_id})"

