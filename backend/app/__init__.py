from .db.database import db
from flask import Flask, render_template
from .config.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    return app
