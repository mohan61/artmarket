import os
from functools import wraps

from flask import abort, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename


def role_required(*roles):
    """Restrict a view to users whose .role is in `roles`."""

    def decorator(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role not in roles:
                abort(403)
            return view_func(*args, **kwargs)

        return wrapped

    return decorator


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


def save_artwork_image(file_storage):
    """Save an uploaded artwork image and return the stored filename, or None."""
    if not file_storage or file_storage.filename == "":
        return None
    if not allowed_file(file_storage.filename):
        return None

    filename = secure_filename(file_storage.filename)
    # Avoid collisions
    base, ext = os.path.splitext(filename)
    target = filename
    counter = 1
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_dir, exist_ok=True)
    while os.path.exists(os.path.join(upload_dir, target)):
        target = f"{base}_{counter}{ext}"
        counter += 1

    file_storage.save(os.path.join(upload_dir, target))
    return target
