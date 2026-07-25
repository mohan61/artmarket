from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from extensions import db
from forms import OrderForm
from models import Artwork, Order
from utils import role_required

customer_bp = Blueprint("customer", __name__, url_prefix="/customer")


@customer_bp.route("/dashboard")
@login_required
@role_required("customer")
def dashboard():
    orders = (
        Order.query.filter_by(customer_id=current_user.id)
        .order_by(Order.order_date.desc())
        .all()
    )
    return render_template("customer/dashboard.html", orders=orders)


@customer_bp.route("/order/<int:artwork_id>", methods=["GET", "POST"])
@login_required
@role_required("customer")
def place_order(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    if artwork.status != "available":
        flash("Sorry, this artwork is no longer available.", "warning")
        return redirect(url_for("main.artwork_detail", artwork_id=artwork.id))

    form = OrderForm(shipping_address=current_user.address or "")
    if form.validate_on_submit():
        total = artwork.price * form.quantity.data
        order = Order(
            customer_id=current_user.id,
            artwork_id=artwork.id,
            quantity=form.quantity.data,
            total_price=total,
            shipping_address=form.shipping_address.data.strip(),
            status="pending",
        )
        artwork.status = "sold"
        db.session.add(order)
        db.session.commit()
        flash("Order placed successfully! Track its status from your dashboard.", "success")
        return redirect(url_for("customer.order_status", order_id=order.id))

    return render_template("customer/order.html", artwork=artwork, form=form)


@customer_bp.route("/order/<int:order_id>/status")
@login_required
@role_required("customer")
def order_status(order_id):
    order = Order.query.get_or_404(order_id)
    if order.customer_id != current_user.id:
        abort(403)
    return render_template("customer/order_status.html", order=order)
