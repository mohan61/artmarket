from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from extensions import db
from forms import ArtworkForm
from models import Artwork, Order
from utils import role_required, save_artwork_image

artist_bp = Blueprint("artist", __name__, url_prefix="/artist")


@artist_bp.route("/dashboard")
@login_required
@role_required("artist")
def dashboard():
    artworks = (
        Artwork.query.filter_by(artist_id=current_user.id)
        .order_by(Artwork.created_at.desc())
        .all()
    )
    artwork_ids = [a.id for a in artworks]
    orders = (
        Order.query.filter(Order.artwork_id.in_(artwork_ids))
        .order_by(Order.order_date.desc())
        .all()
        if artwork_ids
        else []
    )
    return render_template("artist/dashboard.html", artworks=artworks, orders=orders)


@artist_bp.route("/upload", methods=["GET", "POST"])
@login_required
@role_required("artist")
def upload():
    if not current_user.is_approved:
        flash(
            "Your artist account is still pending admin approval. "
            "You'll be able to upload artworks once approved.",
            "warning",
        )
        return redirect(url_for("artist.dashboard"))

    form = ArtworkForm()
    if form.validate_on_submit():
        filename = save_artwork_image(form.image.data)
        artwork = Artwork(
            artist_id=current_user.id,
            title=form.title.data.strip(),
            description=form.description.data,
            price=form.price.data,
            category=form.category.data,
            image_filename=filename,
            status="available",
        )
        db.session.add(artwork)
        db.session.commit()
        flash("Artwork uploaded successfully!", "success")
        return redirect(url_for("artist.dashboard"))

    return render_template("artist/upload.html", form=form)


@artist_bp.route("/artwork/<int:artwork_id>/delete", methods=["POST"])
@login_required
@role_required("artist")
def delete_artwork(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    if artwork.artist_id != current_user.id:
        abort(403)
    db.session.delete(artwork)
    db.session.commit()
    flash("Artwork removed.", "info")
    return redirect(url_for("artist.dashboard"))
