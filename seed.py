"""
Seed the database with mock data: an admin, sample artists (one pending
approval), sample customers, artworks, and orders.

Usage:
    python seed.py            # seeds data (safe to re-run; it wipes & recreates tables)
"""

from decimal import Decimal

from app import create_app
from extensions import db
from models import Artwork, Order, User

app = create_app()


def run():
    with app.app_context():
        print("Dropping and recreating all tables...")
        db.drop_all()
        db.create_all()

        # ---- Admin ----
        admin = User(
            name="Admin User",
            email="admin@artmarket.com",
            role="admin",
            is_approved=True,
        )
        admin.set_password("admin")

        # ---- Artists ----
        artist1 = User(
            name="Elena Ruiz",
            email="mohan@artmarket.com",
            role="artist",
            is_approved=True,
            bio="Contemporary oil painter inspired by coastal landscapes.",
        )
        artist1.set_password("mohanmohan")

        artist2 = User(
            name="Marcus Chen",
            email="marcus@artmarket.test",
            role="artist",
            is_approved=True,
            bio="Digital illustrator and concept artist.",
        )
        artist2.set_password("Artist123!")

        artist3 = User(
            name="Priya Nair",
            email="priya@artmarket.test",
            role="artist",
            is_approved=False,  # pending admin approval
            bio="Sculptor working primarily in clay and bronze.",
        )
        artist3.set_password("Artist123!")

        # ---- Customers ----
        customer1 = User(
            name="Sam Carter",
            email="sam@artmarket.com",
            role="customer",
            is_approved=True,
            address="123 Maple Street, Springfield, USA",
        )
        customer1.set_password("samsam")

        customer2 = User(
            name="Jordan Lee",
            email="jordan@artmarket.test",
            role="customer",
            is_approved=True,
            address="456 Oak Avenue, Rivertown, USA",
        )
        customer2.set_password("Customer123!")

        db.session.add_all(
            [admin, artist1, artist2, artist3, customer1, customer2]
        )
        db.session.commit()

        # ---- Artworks ----
        artworks_data = [
            dict(
                artist_id=artist1.id,
                title="Sunset Over the Bay",
                description="An oil painting capturing warm evening light over calm water.",
                price=Decimal("450.00"),
                category="Painting",
                image_filename="https://picsum.photos/seed/artmarket1/600/600",
            ),
            dict(
                artist_id=artist1.id,
                title="Quiet Harbor",
                description="Soft brushwork depicting a foggy morning harbor scene.",
                price=Decimal("320.00"),
                category="Painting",
                image_filename="https://picsum.photos/seed/artmarket2/600/600",
            ),
            dict(
                artist_id=artist1.id,
                title="Autumn Grove",
                description="A textured landscape of a forest in fall colors.",
                price=Decimal("275.00"),
                category="Painting",
                image_filename="https://picsum.photos/seed/artmarket3/600/600",
                status="sold",
            ),
            dict(
                artist_id=artist2.id,
                title="Neon Skyline",
                description="A vibrant digital illustration of a futuristic city at night.",
                price=Decimal("150.00"),
                category="Digital Art",
                image_filename="https://picsum.photos/seed/artmarket4/600/600",
            ),
            dict(
                artist_id=artist2.id,
                title="Character Concept: Voyager",
                description="Concept art for a sci-fi explorer character.",
                price=Decimal("200.00"),
                category="Illustration",
                image_filename="https://picsum.photos/seed/artmarket5/600/600",
            ),
            dict(
                artist_id=artist2.id,
                title="Cybernetic Bloom",
                description="Digital painting blending organic and mechanical forms.",
                price=Decimal("180.00"),
                category="Digital Art",
                image_filename="https://picsum.photos/seed/artmarket6/600/600",
            ),
        ]

        artworks = [Artwork(**data) for data in artworks_data]
        db.session.add_all(artworks)
        db.session.commit()

        # ---- Orders ----
        sold_artwork = next(a for a in artworks if a.status == "sold")
        available_artwork = next(a for a in artworks if a.status == "available")

        order1 = Order(
            customer_id=customer1.id,
            artwork_id=sold_artwork.id,
            quantity=1,
            total_price=sold_artwork.price,
            shipping_address=customer1.address,
            status="delivered",
        )
        order2 = Order(
            customer_id=customer2.id,
            artwork_id=available_artwork.id,
            quantity=1,
            total_price=available_artwork.price,
            shipping_address=customer2.address,
            status="pending",
        )

        db.session.add_all([order1, order2])
        db.session.commit()

        print("Seed complete.")
        print("-" * 50)
        print("Login credentials:")
        print("  Admin:     admin@artmarket.test    / Admin123!")
        print("  Artist:    elena@artmarket.test     / Artist123!  (approved)")
        print("  Artist:    marcus@artmarket.test     / Artist123!  (approved)")
        print("  Artist:    priya@artmarket.test     / Artist123!  (PENDING approval)")
        print("  Customer:  sam@artmarket.test       / Customer123!")
        print("  Customer:  jordan@artmarket.test    / Customer123!")
        print("-" * 50)


if __name__ == "__main__":
    run()
