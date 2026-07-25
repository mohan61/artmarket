from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from extensions import db
from forms import ArtistRegisterForm, CustomerRegisterForm, LoginForm
from models import User

auth_bp = Blueprint("auth", __name__)


def _redirect_to_dashboard(user):
    if user.is_admin:
        return redirect(url_for("admin.dashboard"))
    if user.is_artist:
        return redirect(url_for("artist.dashboard"))
    return redirect(url_for("customer.dashboard"))


@auth_bp.route("/register")
def register_choice():
    if current_user.is_authenticated:
        return _redirect_to_dashboard(current_user)
    return render_template("register_choice.html")


@auth_bp.route("/register/artist", methods=["GET", "POST"])
def register_artist():
    if current_user.is_authenticated:
        return _redirect_to_dashboard(current_user)

    form = ArtistRegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower().strip()).first():
            flash("An account with that email already exists.", "danger")
            return render_template("register_artist.html", form=form)

        user = User(
            name=form.name.data.strip(),
            email=form.email.data.lower().strip(),
            role="artist",
            is_approved=False,
            bio=form.bio.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash(
            "Registration submitted! An admin will review and approve your artist "
            "account before you can list artworks. You can log in now to check status.",
            "success",
        )
        return redirect(url_for("auth.login"))

    return render_template("register_artist.html", form=form)


@auth_bp.route("/register/customer", methods=["GET", "POST"])
def register_customer():
    if current_user.is_authenticated:
        return _redirect_to_dashboard(current_user)

    form = CustomerRegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower().strip()).first():
            flash("An account with that email already exists.", "danger")
            return render_template("register_customer.html", form=form)

        user = User(
            name=form.name.data.strip(),
            email=form.email.data.lower().strip(),
            role="customer",
            is_approved=True,
            address=form.address.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("Account created! You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register_customer.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return _redirect_to_dashboard(current_user)

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password.", "danger")
            return render_template("login.html", form=form)

        login_user(user)
        flash(f"Welcome back, {user.name}!", "success")
        return _redirect_to_dashboard(user)

    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.landing"))
