import bcrypt
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from app import db
from app.models.food_item import FoodItem
from app.models.order import Order
from app.models.payment import Payment
from app.utils.food_item_forms import FoodItemForm
from app.utils.profile_forms import UpdateProfileForm
from app.utils.decorators import restaurant_required
from flask_login import login_required, current_user
import os
import secrets
from PIL import Image

restaurant = Blueprint("restaurant", __name__)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/uploads', picture_fn)
    
    # Create uploads directory if it doesn't exist
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)
    
    output_size = (300, 300)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    
    return picture_fn

@restaurant.route("/dashboard")
@login_required
@restaurant_required
def dashboard():
    food_items = FoodItem.query.filter_by(restaurant_id=current_user.id).all()
    orders = Order.query.filter_by(restaurant_id=current_user.id).all()
    return render_template("restaurant_dashboard.html", food_items=food_items, orders=orders)

@restaurant.route("/add_food_item", methods=["GET", "POST"])
@login_required
@restaurant_required
def add_food_item():
    form = FoodItemForm()
    if form.validate_on_submit():
        image_url = None
        if form.image.data:
            image_url = save_picture(form.image.data)
        
        food_item = FoodItem(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            image_url=image_url,
            restaurant_id=current_user.id
        )
        db.session.add(food_item)
        db.session.commit()
        flash("Food item has been added!", "success")
        return redirect(url_for("restaurant.dashboard"))
    return render_template("add_food_item.html", title="Add Food Item", form=form)

@restaurant.route("/edit_food_item/<int:food_item_id>", methods=["GET", "POST"])
@login_required
@restaurant_required
def edit_food_item(food_item_id):
    food_item = FoodItem.query.get_or_404(food_item_id)
    if food_item.restaurant_id != current_user.id:
        flash("You can only edit your own food items.", "danger")
        return redirect(url_for("restaurant.dashboard"))
    
    form = FoodItemForm()
    if form.validate_on_submit():
        food_item.name = form.name.data
        food_item.description = form.description.data
        food_item.price = form.price.data
        
        if form.image.data:
            food_item.image_url = save_picture(form.image.data)
        
        db.session.commit()
        flash("Food item has been updated!", "success")
        return redirect(url_for("restaurant.dashboard"))
    elif request.method == "GET":
        form.name.data = food_item.name
        form.description.data = food_item.description
        form.price.data = food_item.price
    
    return render_template("edit_food_item.html", title="Edit Food Item", form=form, food_item=food_item)

@restaurant.route("/delete_food_item/<int:food_item_id>", methods=["POST"])
@login_required
@restaurant_required
def delete_food_item(food_item_id):
    food_item = FoodItem.query.get_or_404(food_item_id)
    if food_item.restaurant_id != current_user.id:
        flash("You can only delete your own food items.", "danger")
        return redirect(url_for("restaurant.dashboard"))
    
    db.session.delete(food_item)
    db.session.commit()
    flash("Food item has been deleted!", "success")
    return redirect(url_for("restaurant.dashboard"))

@restaurant.route("/manage_orders")
@login_required
@restaurant_required
def manage_orders():
    orders = Order.query.filter_by(restaurant_id=current_user.id).all()
    return render_template("manage_orders.html", orders=orders)

@restaurant.route("/update_order_status/<int:order_id>/<status>", methods=["POST"])
@login_required
@restaurant_required
def update_order_status(order_id, status):
    order = Order.query.get_or_404(order_id)
    if order.restaurant_id != current_user.id:
        flash("You can only update your own orders.", "danger")
        return redirect(url_for("restaurant.manage_orders"))
    
    valid_statuses = ['accepted', 'preparing', 'ready', 'delivered', 'cancelled']
    if status in valid_statuses:
        order.status = status
        db.session.commit()
        flash(f"Order status updated to {status}!", "success")
    else:
        flash("Invalid status!", "danger")
    
    return redirect(url_for("restaurant.manage_orders"))

@restaurant.route("/verify_payment/<int:payment_id>", methods=["POST"])
@login_required
@restaurant_required
def verify_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    
    # Check if the payment belongs to an order from this restaurant
    if payment.restaurant_id != current_user.id:
        flash("You can only verify payments for your own orders.", "danger")
        return redirect(url_for("restaurant.manage_orders"))
    
    # Update payment status to verified
    if payment.payment_status == 'pending':
        payment.payment_status = 'verified'
        db.session.commit()
        flash(f"Payment for Order #{payment.order_id} has been verified!", "success")
    else:
        flash("Payment is already verified or has a different status.", "warning")
        return redirect(url_for("restaurant.manage_orders"))

@restaurant.route("/update_payment_status/<int:payment_id>", methods=["POST"])
@login_required
@restaurant_required
def update_payment_status(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    
    # Check if the payment belongs to an order from this restaurant
    if payment.restaurant_id != current_user.id:
        flash("You can only update payments for your own orders.", "danger")
        return redirect(url_for("restaurant.manage_orders"))
    
    new_status = request.form.get("new_status")
    valid_payment_statuses = ["verified", "failed"]

    if new_status in valid_payment_statuses:
        payment.payment_status = new_status
        db.session.commit()
        flash(f"Payment status for Order #{payment.order_id} updated to {new_status}!", "success")
    else:
        flash("Invalid payment status!", "danger")
    
    return redirect(url_for("restaurant.manage_orders"))

@restaurant.route("/profile", methods=["GET", "POST"])
@login_required
@restaurant_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        current_user.location = form.location.data
        if form.password.data:
            current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')        
        db.session.commit()
        flash("Your profile has been updated!", "success")
        return redirect(url_for("restaurant.profile"))
    elif request.method == "GET":
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.location.data = current_user.location
    return render_template("profile.html", title="Profile", form=form)


