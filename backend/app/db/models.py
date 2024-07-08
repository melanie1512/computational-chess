from .database import db
from .database import db

class pieces(db.Model):
    __tablename__ = 'pieces'
    image = db.Column(db.String, nullable=False)
    position_id = db.Column(db.Integer, nulllable=False)
    type = db.Column(db.String, nulllable=False)
    team = db.Column(db.Integer, nullable=False)
    has_moved = db.Column(db.Boolean, nllable=False)
    is_checked = db.Column(db.Boolean, llable=False)
    possible_moves = db.Column(db.JSON, nulllable=False)
    board_id = db.Column(db.Integer, nullable=False)

    def __init__(self, image, position_id, type, team, has_moved, is_checked, possible_moves, board_id):
        self.image = image
        self.position_id = position_id
        self.type = type
        self.team = team
        self.has_moved = has_moved
        self.is_checked = is_checked
        self.possible_moves = possible_moves
        self.board_id = board_id