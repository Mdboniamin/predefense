from flask import session
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
from app.utils.food_item_forms import FoodItemForm
from app.utils.profile_forms import UpdateProfileForm
from flask import jsonify

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

@admin.route("/update_order_status/<int:order_id>", methods=["POST"])
@login_required
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get("new_status")
    valid_statuses = ['pending', 'accepted', 'preparing', 'ready', 'delivered', 'cancelled']
    if new_status in valid_statuses:
        order.status = new_status
        db.session.commit()
        flash(f"Order status updated to {new_status}!", "success")
    else:
        flash("Invalid status!", "danger")
    return redirect(url_for("admin.manage_orders"))

@admin.route("/delete_order/<int:order_id>", methods=["POST"])
@login_required
@admin_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    # Store deletion details in session for potential undo
    session['pending_order_delete'] = {
        'order_id': order.id,
        'food_item_name': order.food_item.name
    }
    session.modified = True
    flash(f"Order '{order.id}' marked for deletion.", "warning")
    return redirect(url_for("admin.manage_orders"))

@admin.route("/undo_delete_order", methods=["POST"])
@login_required
@admin_required
def undo_delete_order():
    if 'pending_order_delete' in session:
        session.pop('pending_order_delete')
        session.modified = True
        flash("Order deletion cancelled!", "success")
    else:
        flash("No order deletion to undo.", "danger")
    return redirect(url_for("admin.manage_orders"))

@admin.route("/confirm_delete_order", methods=["POST"])
@login_required
@admin_required
def confirm_delete_order():
    if 'pending_order_delete' not in session:
        return jsonify({'status': 'error', 'message': 'No pending order deletion'}), 400
    pending = session.pop('pending_order_delete')
    session.modified = True
    order_id = pending['order_id']
    order = Order.query.get_or_404(order_id)
    if order.payment:
        db.session.delete(order.payment)
    db.session.delete(order)
    db.session.commit()
    flash("Order deleted permanently!", "success")
    return jsonify({'status': 'success'}), 200

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
        # Delete related records using relationships
        if user.role == 'restaurant':
            for food_item in user.food_items:
                db.session.delete(food_item)
            for order in user.orders_as_restaurant:
                if order.payment:
                    db.session.delete(order.payment)
                db.session.delete(order)
            for payment in user.payments_as_restaurant:
                db.session.delete(payment)
        elif user.role == 'customer':
            for order in user.orders_as_customer:
                if order.payment:
                    db.session.delete(order.payment)
                db.session.delete(order)
            for payment in user.payments_as_customer:
                db.session.delete(payment)
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
    # Store deletion details in session for potential undo
    session['pending_delete'] = {
        'food_item_id': food_item.id,
        'food_item_name': food_item.name,
        'orders': [(order.id, order.payment.id if order.payment else None) for order in Order.query.filter_by(food_item_id=food_item.id).all()]
    }
    session.modified = True
    flash(f"Food item '{food_item.name}' marked for deletion.", "warning")
    return redirect(url_for("admin.manage_food_items"))

@admin.route("/undo_delete_food_item", methods=["POST"])
@login_required
@admin_required
def undo_delete_food_item():
    if 'pending_delete' in session:
        session.pop('pending_delete')
        session.modified = True
        flash("Deletion cancelled!", "success")
    else:
        flash("No deletion to undo.", "danger")
    return redirect(url_for("admin.manage_food_items"))

@admin.route("/confirm_delete_food_item", methods=["POST"])
@login_required
@admin_required
def confirm_delete_food_item():
    if 'pending_delete' not in session:
        return jsonify({'status': 'error', 'message': 'No pending deletion'}), 400
    pending = session.pop('pending_delete')
    session.modified = True
    food_item_id = pending['food_item_id']
    food_item = FoodItem.query.get_or_404(food_item_id)
    orders = Order.query.filter_by(food_item_id=food_item_id).all()
    for order in orders:
        if order.payment:
            db.session.delete(order.payment)
        db.session.delete(order)
    db.session.delete(food_item)
    db.session.commit()
    flash("Food item deleted permanently!", "success")
    return jsonify({'status': 'success'}), 200

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

@admin.route("/profile", methods=["GET", "POST"])
@login_required
@admin_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        current_user.location = form.location.data
        db.session.commit()
        flash("Your profile has been updated!", "success")
        return redirect(url_for("admin.profile"))
    elif request.method == "GET":
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.location.data = current_user.location
    total_users = User.query.count()
    total_food_items = FoodItem.query.count()
    total_orders = Order.query.count()
    total_payments = Payment.query.count()
    return render_template("profile.html", title="Profile", form=form, total_users=total_users, total_food_items=total_food_items, total_orders=total_orders, total_payments=total_payments)