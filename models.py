from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # 'artist', 'customer', or 'admin'
    role = db.Column(db.String(20), nullable=False, default="customer")

    # Only meaningful for artists: must be approved by an admin before selling
    is_approved = db.Column(db.Boolean, default=False, nullable=False)

    bio = db.Column(db.Text)
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    artworks = db.relationship(
        "Artwork", backref="artist", lazy=True, foreign_keys="Artwork.artist_id"
    )
    orders = db.relationship(
        "Order", backref="customer", lazy=True, foreign_keys="Order.customer_id"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_artist(self):
        return self.role == "artist"

    @property
    def is_customer(self):
        return self.role == "customer"

    @property
    def is_admin(self):
        return self.role == "admin"

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Artwork(db.Model):
    __tablename__ = "artworks"

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(80))

    # Either a filename inside static/uploads OR a full http(s) URL (used by seed data)
    image_filename = db.Column(db.String(500))

    # 'available' or 'sold'
    status = db.Column(db.String(20), default="available", nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship("Order", backref="artwork", lazy=True)

    @property
    def image_url(self):
        if not self.image_filename:
            return None
        if self.image_filename.startswith("http://") or self.image_filename.startswith(
            "https://"
        ):
            return self.image_filename
        from flask import url_for

        return url_for("static", filename=f"uploads/{self.image_filename}")

    def __repr__(self):
        return f"<Artwork {self.title}>"


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey("artworks.id"), nullable=False)

    quantity = db.Column(db.Integer, default=1, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    shipping_address = db.Column(db.String(255), nullable=False)

    # pending -> confirmed -> shipped -> delivered  (or cancelled)
    status = db.Column(db.String(30), default="pending", nullable=False)

    order_date = db.Column(db.DateTime, default=datetime.utcnow)

    STATUS_FLOW = ["pending", "confirmed", "shipped", "delivered"]

    def __repr__(self):
        return f"<Order #{self.id} - {self.status}>"
