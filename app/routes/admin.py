from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.food_item import FoodItem
from app.models.order import Order
from app.models.payment import Payment
from app.utils.decorators import admin_required

admin = Blueprint("admin", __name__)

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

@admin.route("/approve_restaurant/<int:user_id>")
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
        payment.order.status = "accepted" # Update order status as well
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
        payment.payment_status = "rejected"
        payment.order.status = "cancelled" # Update order status as well
        db.session.commit()
        flash("Payment rejected successfully!", "success")
    else:
        flash("Invalid payment status.", "danger")
    return redirect(url_for("admin.manage_payments"))

