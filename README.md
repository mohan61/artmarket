# ArtMarket — Online Art Marketplace

A full-stack demo art marketplace built with **Flask**, **PostgreSQL**, **SQLAlchemy**,
**Jinja2**, and plain **HTML/CSS/JS**.

Artists can register and (after admin approval) upload artworks for sale. Customers can
register, browse the public gallery, place orders, and track order status. Admins approve/reject
artist registrations and manage order statuses.

---

## Features

- **Landing page** with featured artworks and platform stats
- **Public gallery** — anyone (including guests) can browse/search/filter artworks
- **Artwork detail page**
- **Single login page** for all roles (artist / customer / admin), session-based auth with hashed passwords
- **Separate registration flows** for Artists and Customers
  - Artist accounts require **admin approval** before they can upload artwork
- **Role-based dashboards**
  - *Artist:* approval status, my artworks, orders placed on my artworks, delete artwork
  - *Customer:* order history, order status tracker
  - *Admin:* approve/reject pending artists, view all users, view & update every order's status
- **Artwork upload page** (title, description, price, category, image)
- **Order placement page** (quantity, shipping address)
- **Order status page** with a visual pending → confirmed → shipped → delivered tracker
- **Seed script** with mock admin/artist/customer/artwork/order data
- CSRF protection (Flask-WTF), password hashing (Werkzeug), role-guarded routes

---

## Tech Stack

| Layer      | Technology                              |
|------------|------------------------------------------|
| Backend    | Flask 3, Flask-Login, Flask-WTF          |
| Database   | PostgreSQL + Flask-SQLAlchemy (ORM)      |
| Templates  | Jinja2                                   |
| Frontend   | HTML5, CSS3 (custom, no framework), JS   |

---

## Project Structure

```
artmarket/
├── app.py                  # App factory + entrypoint
├── config.py                # Config (reads .env)
├── extensions.py             # db, login_manager, csrf singletons
├── models.py                 # User, Artwork, Order models
├── forms.py                  # Flask-WTF forms
├── utils.py                   # role_required decorator, image upload helper
├── seed.py                    # Mock data seeder (DROPS & recreates tables)
├── requirements.txt
├── .env.example
├── .gitignore
├── .vscode/launch.json        # VS Code "Run and Debug" config
├── blueprints/
│   ├── main.py               # landing, gallery, artwork detail
│   ├── auth.py                # register (artist/customer), login, logout
│   ├── artist.py               # artist dashboard, upload, delete
│   ├── customer.py             # customer dashboard, place order, order status
│   └── admin.py                # admin dashboard, approve/reject, update order status
├── templates/
│   ├── base.html, landing.html, gallery.html, artwork_detail.html
│   ├── login.html, register_choice.html, register_artist.html, register_customer.html
│   ├── artist/dashboard.html, artist/upload.html
│   ├── customer/dashboard.html, customer/order.html, customer/order_status.html
│   ├── admin/dashboard.html
│   └── errors/403.html, errors/404.html
└── static/
    ├── css/style.css
    ├── js/main.js
    └── uploads/               # artist-uploaded images land here
```

---

## 1. Prerequisites

- **Python 3.10+**
- **PostgreSQL 13+** installed and running locally (or a remote instance)
- **VS Code** with the *Python* extension (ms-python.python)
- `pip` / `venv`

---

## 2. Set up PostgreSQL

Open `psql` (or pgAdmin) and create a database:

```sql
CREATE DATABASE artmarket;
```

(Optional) Create a dedicated user:

```sql
CREATE USER artmarket_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE artmarket TO artmarket_user;
```

You'll reference this database in your `DATABASE_URL` (step 4).

---

## 3. Open the project in VS Code

1. Unzip this project and open the `artmarket/` folder in VS Code (`File → Open Folder...`).
2. Open a terminal in VS Code: `` Ctrl+` `` (or `View → Terminal`).

---

## 4. Create a virtual environment & install dependencies

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

In VS Code, select this virtual environment as your Python interpreter:
`Ctrl+Shift+P` → `Python: Select Interpreter` → choose `./venv`.

---

## 5. Configure environment variables

Copy the example env file and edit it:

```bash
cp .env.example .env        # macOS/Linux
copy .env.example .env      # Windows
```

Edit `.env`:

```
SECRET_KEY=some-long-random-string
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/artmarket
```

Adjust the username/password/host/port/db name to match what you created in step 2.

---

## 6. Create tables & seed mock data

The `seed.py` script creates all tables (via SQLAlchemy, no separate migration tool needed
for this demo) and populates mock data:

```bash
python seed.py
```

This will print out the seeded login credentials, e.g.:

```
Admin:     admin@artmarket.test    / Admin123!
Artist:    elena@artmarket.test    / Artist123!   (approved)
Artist:    marcus@artmarket.test   / Artist123!   (approved)
Artist:    priya@artmarket.test    / Artist123!   (PENDING approval)
Customer:  sam@artmarket.test      / Customer123!
Customer:  jordan@artmarket.test   / Customer123!
```

> ⚠️ `seed.py` calls `db.drop_all()` — re-running it wipes and recreates the schema. Use it
> freely in development; don't run it against a database with real data you want to keep.

---

## 7. Run the app

**Option A — VS Code Run & Debug:**
Press `F5` (uses the included `.vscode/launch.json` config: "Flask (app.py)").

**Option B — terminal:**
```bash
flask --app app run --debug
```
or simply:
```bash
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

---

## 8. Try it out

- Visit the landing page and browse the **Gallery** as a guest.
- Log in as `elena@artmarket.test` (approved artist) → go to **Dashboard** → **Upload New Artwork**.
- Log in as `priya@artmarket.test` (pending artist) → see the "pending approval" notice.
- Log in as `admin@artmarket.test` → **Admin** dashboard → approve Priya, update order statuses.
- Log in as `sam@artmarket.test` or `jordan@artmarket.test` (customers) → browse the gallery,
  place an order on an available artwork, then track it from **Dashboard → Track**.
- Register your own new Artist or Customer account from the **Register** page.

---

## Notes & Design Decisions

- **Artist approval workflow:** new artist accounts are created with `is_approved=False`.
  They can log in and see their dashboard, but cannot upload artwork until an admin approves
  them from the Admin dashboard. Customer accounts don't require approval.
- **Order status flow:** `pending → confirmed → shipped → delivered` (or `cancelled`). Only
  admins can change an order's status in this demo; customers can view/track it.
- **Images:** artists can optionally upload an image file (stored under `static/uploads/`).
  If skipped, a colored placeholder is shown. Seed data uses external placeholder image URLs
  (picsum.photos) so the demo looks populated without shipping binary image files.
- **CSRF protection** is enabled globally via Flask-WTF; all POST forms include a CSRF token.
- **Passwords** are hashed with Werkzeug's `generate_password_hash` / `check_password_hash` —
  plaintext passwords are never stored.
- This project uses `db.create_all()` (via `seed.py`) rather than a migrations framework
  (e.g. Flask-Migrate/Alembic) to keep the demo simple. For a production app, add
  Flask-Migrate for proper schema migrations.

---

## Troubleshooting

- **`psycopg2` install errors:** ensure PostgreSQL client dev headers are installed, or rely
  on the bundled `psycopg2-binary` (already in `requirements.txt`) which avoids compiling from source.
- **`sqlalchemy.exc.OperationalError: could not connect`:** double-check PostgreSQL is running
  and that `DATABASE_URL` in `.env` matches your actual host/port/user/password/db name.
- **Login redirect loop / CSRF errors:** make sure `SECRET_KEY` is set in `.env` and the server
  was restarted after editing `.env`.
- **Uploaded images not showing:** confirm the `static/uploads/` folder exists and is writable;
  it's created automatically on first upload if missing.

---

## License

Demo project for educational/portfolio purposes.
