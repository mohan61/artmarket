from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required

from extensions import db
from models import Artwork, Order, User
from utils import role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@login_required
@role_required("admin")
def dashboard():
    pending_artists = (
        User.query.filter_by(role="artist", is_approved=False)
        .order_by(User.created_at.desc())
        .all()
    )
    all_artists = User.query.filter_by(role="artist").order_by(User.created_at.desc()).all()
    all_customers = User.query.filter_by(role="customer").order_by(User.created_at.desc()).all()
    all_orders = Order.query.order_by(Order.order_date.desc()).all()

    stats = {
        "total_users": User.query.count(),
        "total_artists": len(all_artists),
        "total_customers": len(all_customers),
        "total_artworks": Artwork.query.count(),
        "total_orders": len(all_orders),
        "pending_approvals": len(pending_artists),
    }

    return render_template(
        "admin/dashboard.html",
        pending_artists=pending_artists,
        all_artists=all_artists,
        all_customers=all_customers,
        all_orders=all_orders,
        stats=stats,
        order_flow=Order.STATUS_FLOW,
    )


@admin_bp.route("/artist/<int:user_id>/approve", methods=["POST"])
@login_required
@role_required("admin")
def approve_artist(user_id):
    user = User.query.get_or_404(user_id)
    if user.role != "artist":
        abort(400)
    user.is_approved = True
    db.session.commit()
    flash(f"{user.name} has been approved as an artist.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/artist/<int:user_id>/reject", methods=["POST"])
@login_required
@role_required("admin")
def reject_artist(user_id):
    user = User.query.get_or_404(user_id)
    if user.role != "artist":
        abort(400)
    db.session.delete(user)
    db.session.commit()
    flash(f"{user.name}'s artist registration has been rejected and removed.", "info")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/order/<int:order_id>/update", methods=["POST"])
@login_required
@role_required("admin")
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get("status")
    valid_statuses = Order.STATUS_FLOW + ["cancelled"]
    if new_status not in valid_statuses:
        abort(400)
    order.status = new_status
    db.session.commit()
    flash(f"Order #{order.id} status updated to '{new_status}'.", "success")
    return redirect(url_for("admin.dashboard"))
