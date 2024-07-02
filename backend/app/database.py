from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

load_dotenv()

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = (
          os.getenv("SQLALCHEMY_DATABASE_URI")# Cambia esto con tus credenciales y nombre de la base de datos
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
