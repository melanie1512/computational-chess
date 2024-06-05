from flask import Flask
from database import init_db
from models import Piece, Position

def create_app():
    app = Flask(__name__)
    init_db(app)

    with app.app_context():
        db.create_all()

    return app
