from app import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('pending', 'accepted', 'preparing', 'ready', 'delivered', 'cancelled', name='order_status'), default='pending')
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)

    payment = db.relationship("Payment", backref="order", uselist=False, foreign_keys="Order.payment_id")
    def __repr__(self):
        return f"Order(ID: {self.id}, Customer: {self.customer_id}, Status: {self.status})"

