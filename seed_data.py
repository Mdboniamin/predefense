from app import create_app, db, bcrypt
from app.models.user import User
from app.models.food_item import FoodItem
from app.models.order import Order
from app.models.payment import Payment
from decimal import Decimal

def seed_data():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create users
        hashed_admin_password = bcrypt.generate_password_hash("admin123").decode("utf-8")
        admin = User(name="Admin User", email="admin@foodapp.com", phone_number="01000000000", location="Admin City", password=hashed_admin_password, role="admin", status="active")
        db.session.add(admin)

        hashed_restaurant_password = bcrypt.generate_password_hash("restaurant123").decode("utf-8")
        restaurant1 = User(name="Taste of Italy", email="restaurant@foodapp.com", phone_number="01111111111", location="Dhaka", password=hashed_restaurant_password, role="restaurant", status="active")
        restaurant2 = User(name="Spice Route", email="spice@foodapp.com", phone_number="01222222222", location="Chittagong", password=hashed_restaurant_password, role="restaurant", status="pending")
        db.session.add(restaurant1)
        db.session.add(restaurant2)

        hashed_customer_password = bcrypt.generate_password_hash("customer123").decode("utf-8")
        customer1 = User(name="John Doe", email="customer@foodapp.com", phone_number="01333333333", location="Sylhet", password=hashed_customer_password, role="customer", status="active")
        customer2 = User(name="Jane Smith", email="jane@foodapp.com", phone_number="01444444444", location="Khulna", password=hashed_customer_password, role="customer", status="active")
        db.session.add(customer1)
        db.session.add(customer2)
        db.session.commit()

        # Create food items
        pizza = FoodItem(name="Margherita Pizza", description="Classic pizza with tomato and mozzarella", price=Decimal("12.50"), restaurant_id=restaurant1.id, image_url="pizza.jpg")
        pasta = FoodItem(name="Carbonara Pasta", description="Creamy pasta with egg, cheese, and bacon", price=Decimal("14.00"), restaurant_id=restaurant1.id, image_url="pasta.jpg")
        biryani = FoodItem(name="Chicken Biryani", description="Fragrant basmati rice with spiced chicken", price=Decimal("10.00"), restaurant_id=restaurant2.id, image_url="biryani.jpg")
        curry = FoodItem(name="Vegetable Curry", description="Mixed vegetables in a rich, spicy sauce", price=Decimal("9.50"), restaurant_id=restaurant2.id, image_url="curry.jpg")
        db.session.add_all([pizza, pasta, biryani, curry])
        db.session.commit()

        # Create orders and payments
        order1 = Order(customer_id=customer1.id, food_item_id=pizza.id, restaurant_id=restaurant1.id, quantity=1, total_price=pizza.price, status="pending")
        db.session.add(order1)
        db.session.flush()
        payment1 = Payment(order_id=order1.id, customer_id=customer1.id, restaurant_id=restaurant1.id, bkash_transaction_id="TXN123456789", payment_phone_number="01333333333", amount=pizza.price, payment_status="pending")
        db.session.add(payment1)
        order1.payment_id = payment1.id

        order2 = Order(customer_id=customer2.id, food_item_id=biryani.id, restaurant_id=restaurant2.id, quantity=2, total_price=biryani.price * 2, status="accepted")
        db.session.add(order2)
        db.session.flush()
        payment2 = Payment(order_id=order2.id, customer_id=customer2.id, restaurant_id=restaurant2.id, bkash_transaction_id="TXN987654321", payment_phone_number="01444444444", amount=biryani.price * 2, payment_status="verified")
        db.session.add(payment2)
        order2.payment_id = payment2.id
        
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()

