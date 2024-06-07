from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://postgres:1234@localhost:5432/chess_db"  # Cambia esto con tus credenciales y nombre de la base de datos
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
