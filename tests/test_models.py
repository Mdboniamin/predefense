import unittest
from app import create_app, db
from app.models.user import User
from app.models.food_item import FoodItem
from app.models.order import Order
from app.models.payment import Payment
from decimal import Decimal

class ModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app.config["TESTING"] = True
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_model(self):
        with self.app.app_context():
            user = User(name="Test User", email="test@example.com", phone_number="1234567890", location="Test Location", password="hashed_password", role="customer")
            db.session.add(user)
            db.session.commit()
            self.assertEqual(user.name, "Test User")
            self.assertEqual(user.role, "customer")

    def test_food_item_model(self):
        with self.app.app_context():
            restaurant = User(name="Test Restaurant", email="restaurant@example.com", phone_number="0987654321", location="Restaurant Location", password="hashed_password", role="restaurant")
            db.session.add(restaurant)
            db.session.commit()

            food_item = FoodItem(name="Test Food", description="Delicious food", price=Decimal("10.99"), restaurant_id=restaurant.id)
            db.session.add(food_item)
            db.session.commit()
            self.assertEqual(food_item.name, "Test Food")
            self.assertEqual(food_item.price, Decimal("10.99"))

    def test_order_model(self):
        with self.app.app_context():
            customer = User(name="Test Customer", email="customer@example.com", phone_number="1111111111", location="Customer Location", password="hashed_password", role="customer")
            restaurant = User(name="Test Restaurant", email="restaurant@example.com", phone_number="2222222222", location="Restaurant Location", password="hashed_password", role="restaurant")
            db.session.add(customer)
            db.session.add(restaurant)
            db.session.commit()

            food_item = FoodItem(name="Test Food", description="Delicious food", price=Decimal("10.99"), restaurant_id=restaurant.id)
            db.session.add(food_item)
            db.session.commit()

            order = Order(customer_id=customer.id, food_item_id=food_item.id, restaurant_id=restaurant.id, quantity=2, total_price=Decimal("21.98"))
            db.session.add(order)
            db.session.commit()
            self.assertEqual(order.quantity, 2)
            self.assertEqual(order.total_price, Decimal("21.98"))

    def test_payment_model(self):
        with self.app.app_context():
            customer = User(name="Test Customer", email="customer@example.com", phone_number="1111111111", location="Customer Location", password="hashed_password", role="customer")
            restaurant = User(name="Test Restaurant", email="restaurant@example.com", phone_number="2222222222", location="Restaurant Location", password="hashed_password", role="restaurant")
            db.session.add(customer)
            db.session.add(restaurant)
            db.session.commit()

            food_item = FoodItem(name="Test Food", description="Delicious food", price=Decimal("10.99"), restaurant_id=restaurant.id)
            db.session.add(food_item)
            db.session.commit()

            order = Order(customer_id=customer.id, food_item_id=food_item.id, restaurant_id=restaurant.id, quantity=2, total_price=Decimal("21.98"))
            db.session.add(order)
            db.session.commit()

            payment = Payment(order_id=order.id, customer_id=customer.id, restaurant_id=restaurant.id, bkash_transaction_id="TXN123456", payment_phone_number="1111111111", amount=Decimal("21.98"))
            db.session.add(payment)
            db.session.commit()
            self.assertEqual(payment.bkash_transaction_id, "TXN123456")
            self.assertEqual(payment.amount, Decimal("21.98"))

if __name__ == "__main__":
    unittest.main()

