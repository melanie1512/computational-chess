from .db.database import db, migrate
from flask import Flask, render_template
from .config.config import Config
from .endpoints import app as homeViews

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(homeViews)
    migrate.init_app(app, db)        # Flask DB Migration

    return app

def register_error_handlers(app):

    @app.errorhandler(500)
    def base_error_handler(e):
        return 500

    @app.errorhandler(404)
    def error_404_handler(e):
        return 404