from .db.database import db
from flask import Flask, render_template
from .config.config import Config
from flask import Flask, jsonify, request, render_template
from .db.database import db, setup_db
from .models.Board import Board
from .models.Position import Position
from .models.Types import PieceType, TeamType
from .models.Piece import Piece
from dotenv import load_dotenv
import os
from .endpoints import app as endpoints

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    path = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config.from_object(Config)
    setup_db(app, path)

    with app.app_context():
        db.create_all()

    return app

app = create_app()
app.register_blueprint(endpoints)