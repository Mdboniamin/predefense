from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.food_item import FoodItem
from app.models.order import Order
from app.models.payment import Payment
from app.utils.decorators import admin_required
import os
import secrets
from PIL import Image
from flask import current_app

admin = Blueprint("admin", __name__)
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/uploads', picture_fn)
    
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)
    
    output_size = (300, 300)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    
    return picture_fn
@admin.route("/dashboard")
@login_required
@admin_required
def dashboard():
    users = User.query.all()
    food_items = FoodItem.query.all()
    orders = Order.query.all()
    payments = Payment.query.all()
    return render_template("admin_dashboard.html", users=users, food_items=food_items, orders=orders, payments=payments)

@admin.route("/manage_users")
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template("manage_users.html", users=users)

@admin.route("/approve_restaurant/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def approve_restaurant(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == "restaurant" and user.status == "pending":
        user.status = "active"
        db.session.commit()
        flash("Restaurant approved successfully!", "success")
    else:
        flash("Invalid request.", "danger")
    return redirect(url_for("admin.manage_users"))

@admin.route("/suspend_user/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def suspend_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role != "admin":
        user.status = "suspended"
        db.session.commit()
        flash("User suspended successfully!", "success")
    else:
        flash("Cannot suspend an admin user.", "danger")
    return redirect(url_for("admin.manage_users"))

@admin.route("/activate_user/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def activate_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role != "admin":
        user.status = "active"
        db.session.commit()
        flash("User activated successfully!", "success")
    else:
        flash("Cannot activate an admin user.", "danger")
    return redirect(url_for("admin.manage_users"))

@admin.route("/manage_food_items")
@login_required
@admin_required
def manage_food_items():
    food_items = FoodItem.query.all()
    return render_template("manage_food_items.html", food_items=food_items)

@admin.route("/manage_orders")
@login_required
@admin_required
def manage_orders():
    orders = Order.query.all()
    return render_template("manage_orders.html", orders=orders)

@admin.route("/manage_payments")
@login_required
@admin_required
def manage_payments():
    payments = Payment.query.all()
    return render_template("admin_manage_payments.html", payments=payments)

@admin.route("/verify_payment/<int:payment_id>", methods=["POST"])
@login_required
@admin_required
def verify_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    if payment.payment_status == "pending":
        payment.payment_status = "verified"
        payment.order.status = "accepted"
        db.session.commit()
        flash("Payment verified successfully!", "success")
    else:
        flash("Invalid payment status.", "danger")
    return redirect(url_for("admin.manage_payments"))

@admin.route("/reject_payment/<int:payment_id>", methods=["POST"])
@login_required
@admin_required
def reject_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    if payment.payment_status == "pending":
        payment.payment_status = "failed"
        payment.order.status = "cancelled"
        db.session.commit()
        flash("Payment rejected successfully!", "success")
    else:
        flash("Invalid payment status.", "danger")
    return redirect(url_for("admin.manage_payments"))

@admin.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role != "admin":
        # Delete related food items, orders, and payments
        FoodItem.query.filter_by(restaurant_id=user.id).delete()
        Order.query.filter_by(restaurant_id=user.id).delete()
        Payment.query.filter_by(restaurant_id=user.id).delete()
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully!", "success")
    else:
        flash("Cannot delete an admin user.", "danger")
    return redirect(url_for("admin.manage_users"))

@admin.route("/delete_food_item/<int:food_item_id>", methods=["POST"])
@login_required
@admin_required
def delete_food_item(food_item_id):
    food_item = FoodItem.query.get_or_404(food_item_id)
    # Delete related orders and payments
    Order.query.filter_by(food_item_id=food_item.id).delete()
    Payment.query.join(Order).filter(Order.food_item_id == food_item.id).delete()
    db.session.delete(food_item)
    db.session.commit()
    flash("Food item deleted successfully!", "success")
    return redirect(url_for("admin.manage_food_items"))

@admin.route("/edit_food_item/<int:food_item_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_food_item(food_item_id):
    food_item = FoodItem.query.get_or_404(food_item_id)
    form = FoodItemForm()
    if form.validate_on_submit():
        food_item.name = form.name.data
        food_item.description = form.description.data
        food_item.price = form.price.data
        if form.image.data:
            image_url = save_picture(form.image.data)
            food_item.image_url = image_url
        db.session.commit()
        flash("Food item updated successfully!", "success")
        return redirect(url_for("admin.manage_food_items"))
    elif request.method == "GET":
        form.name.data = food_item.name
        form.description.data = food_item.description
        form.price.data = food_item.price
    return render_template("edit_food_item.html", title="Edit Food Item", form=form, food_item=food_item)