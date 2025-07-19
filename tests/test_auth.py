import unittest
from flask import current_app
from app import create_app, db, bcrypt
from app.models.user import User

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_registration(self):
        with self.app.app_context():
            hashed_password = bcrypt.generate_password_hash("password").decode("utf-8")
            user = User(name="Test User", email="test@example.com", phone_number="1234567890", location="Test Location", password=hashed_password, role="customer")
            db.session.add(user)
            db.session.commit()
            self.assertIsNotNone(user.id)

    def test_login(self):
        with self.app.app_context():
            hashed_password = bcrypt.generate_password_hash("password").decode("utf-8")
            user = User(name="Test User", email="test@example.com", phone_number="1234567890", location="Test Location", password=hashed_password, role="customer")
            db.session.add(user)
            db.session.commit()

            response = self.client.post("/auth/login", data=dict(
                email="test@example.com",
                password="password"
            ), follow_redirects=True)
            self.assertIn(b"Welcome to Food Order App", response.data)

    def test_login_invalid_password(self):
        with self.app.app_context():
            hashed_password = bcrypt.generate_password_hash("password").decode("utf-8")
            user = User(name="Test User", email="test@example.com", phone_number="1234567890", location="Test Location", password=hashed_password, role="customer")
            db.session.add(user)
            db.session.commit()

            response = self.client.post("/auth/login", data=dict(
                email="test@example.com",
                password="wrong_password"
            ), follow_redirects=True)
            self.assertIn(b"Login Unsuccessful. Please check email and password", response.data)

if __name__ == "__main__":
    unittest.main()

