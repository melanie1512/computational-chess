from flask import Flask
from .database import init_db, db
from .models.models import Piece, Position


def create_app():
    app = Flask(__name__)
    init_db(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
