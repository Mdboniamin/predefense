# Food Order App

A multi-user role-based CRUD food ordering system with payment tracking using Flask, SQLAlchemy, and bKash payment integration.

## Features

### Customer Features
- Browse food items from different restaurants
- Add items to cart and place orders
- Make payments via bKash (manual verification)
- Track order history and status
- Update profile information

### Restaurant Features
- Manage food items (add, edit, delete)
- View and manage orders
- Update order status (pending → accepted → preparing → ready → delivered)
- View payment details
- Update profile information

### Admin Features
- Manage all users, food items, and orders
- Approve restaurant accounts
- Verify bKash payments
- Full system oversight

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (development) / MySQL (production)
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Authentication**: Flask-Login with bcrypt password hashing
- **Payment**: Manual bKash payment with transaction ID verification
- **Security**: CSRF protection, input validation

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd food_order_app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables (optional):
```bash
export SECRET_KEY="your-secret-key"
export DATABASE_URL="your-database-url"
```

4. Initialize the database:
```bash
python run.py
```

5. Access the application at `http://localhost:5000`

## Demo Users

The application comes with pre-seeded demo users:

### Admin
- **Email**: admin@foodapp.com
- **Password**: admin123

### Restaurant
- **Email**: restaurant@foodapp.com
- **Password**: restaurant123

### Customer
- **Email**: customer@foodapp.com
- **Password**: customer123

## Usage

1. **Registration**: Users can register as Customer or Restaurant
2. **Restaurant Approval**: Restaurant accounts need admin approval
3. **Food Management**: Restaurants can add/edit their food items
4. **Ordering**: Customers browse and add items to cart
5. **Payment**: Manual bKash payment with transaction ID
6. **Order Tracking**: Real-time order status updates

## Database Schema

### Users Table
- id, name, email, phone_number, location, password, role, status

### Food Items Table
- id, name, description, price, image_url, restaurant_id, created_at

### Orders Table
- id, customer_id, food_item_id, restaurant_id, quantity, total_price, status, payment_id, order_date

### Payments Table
- id, order_id, customer_id, restaurant_id, bkash_transaction_id, payment_phone_number, payment_method, amount, payment_status, payment_date

## Security Features

- Password hashing with bcrypt
- CSRF protection on all forms
- Role-based access control
- Input validation and sanitization
- Session management

## Testing

Run the test suite:
```bash
python -m unittest discover tests
```

## Deployment

For production deployment:

1. Set up a MySQL database
2. Update the DATABASE_URL environment variable
3. Set a secure SECRET_KEY
4. Use a production WSGI server like Gunicorn
5. Configure a reverse proxy (Nginx)

## License

This project is licensed under the MIT License.

