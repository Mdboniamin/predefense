from app import db
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bkash_transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    payment_phone_number = db.Column(db.String(20), nullable=False)
    payment_method = db.Column(db.Enum('bkash', name='payment_methods'), default='bkash')
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.Enum('pending', 'verified','rejected' ,'failed', name='payment_status'), default='pending' )
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Payment(ID: {self.id}, Transaction: {self.bkash_transaction_id}, Status: {self.payment_status})"

