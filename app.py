from flask import Flask, render_template

from config import Config
from extensions import csrf, db, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from blueprints.main import main_bp
    from blueprints.auth import auth_bp
    from blueprints.artist import artist_bp
    from blueprints.customer import customer_bp
    from blueprints.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(artist_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.context_processor
    def inject_globals():
        from datetime import datetime

        return {"current_year": datetime.utcnow().year}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
