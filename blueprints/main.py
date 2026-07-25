from flask import Blueprint, render_template, request

from extensions import db
from models import Artwork, User

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def landing():
    featured = (
        Artwork.query.filter_by(status="available")
        .order_by(Artwork.created_at.desc())
        .limit(6)
        .all()
    )
    artist_count = User.query.filter_by(role="artist", is_approved=True).count()
    artwork_count = Artwork.query.filter_by(status="available").count()
    return render_template(
        "landing.html",
        featured=featured,
        artist_count=artist_count,
        artwork_count=artwork_count,
    )


@main_bp.route("/gallery")
def gallery():
    category = request.args.get("category", "").strip()
    q = request.args.get("q", "").strip()

    query = Artwork.query.filter_by(status="available")
    if category:
        query = query.filter(Artwork.category.ilike(f"%{category}%"))
    if q:
        query = query.filter(Artwork.title.ilike(f"%{q}%"))

    artworks = query.order_by(Artwork.created_at.desc()).all()

    categories = sorted(
        {
            c[0]
            for c in db.session.query(Artwork.category)
            .filter(Artwork.category.isnot(None))
            .distinct()
        }
    )

    return render_template(
        "gallery.html",
        artworks=artworks,
        categories=categories,
        current_category=category,
        q=q,
    )


@main_bp.route("/artwork/<int:artwork_id>")
def artwork_detail(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    return render_template("artwork_detail.html", artwork=artwork)
