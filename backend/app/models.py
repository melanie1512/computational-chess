from database import db

class Position(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)

    def same_position(self, other_position):
        return self.x == other_position.x and self.y == other_position.y

    def clone(self):
        return Position(x=self.x, y=self.y)

class Piece(db.Model):
    __tablename__ = 'pieces'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'), nullable=False)
    position = db.relationship('Position', backref=db.backref('pieces', lazy=True))
    type = db.Column(db.String, nullable=False)
    team = db.Column(db.Integer, nullable=False)
    has_moved = db.Column(db.Boolean, default=False)
    is_checked = db.Column(db.Boolean, default=False)

    def __init__(self, position, type, team, has_moved=False, possible_moves=None):
        if possible_moves is None:
            possible_moves = []
        self.image = f'assets/images/{type}_{"w" if team == 1 else "b"}.png'
        self.position = position
        self.type = type
        self.team = team
        self.possible_moves = possible_moves
        self.has_moved = has_moved
        self.is_checked = False

    @property
    def is_pawn(self):
        return self.type == PieceType.PAWN

    @property
    def is_rook(self):
        return self.type == PieceType.ROOK

    @property
    def is_knight(self):
        return self.type == PieceType.KNIGHT

    @property
    def is_bishop(self):
        return self.type == PieceType.BISHOP

    @property
    def is_king(self):
        return self.type == PieceType.KING

    @property
    def is_queen(self):
        return self.type == PieceType.QUEEN

    def same_piece_position(self, other_piece):
        return self.position.same_position(other_piece.position)

    def same_position(self, other_position):
        return self.position.same_position(other_position)

    def clone(self):
        return Piece(
            position=self.position.clone(),
            type=self.type,
            team=self.team,
            has_moved=self.has_moved,
            possible_moves=[pos.clone() for pos in self.possible_moves]
        )

class TeamTypeManager:
    def __init__(self, our):
        self._our = 1 if our == 'w' else 2
        self._opponent = 2 if our == 'w' else 1

    @property
    def our(self):
        return self._our

    @our.setter
    def our(self, value):
        self._our = 1 if value == 'w' else 2

    @property
    def opponent(self):
        return self._opponent

    @opponent.setter
    def opponent(self, value):
        self._opponent = 2 if value == 'w' else 1

TeamTypeManager_ = TeamTypeManager('w')

class PieceType:
    PAWN = 'pawn'
    BISHOP = 'bishop'
    KNIGHT = 'knight'
    ROOK = 'rook'
    QUEEN = 'queen'
    KING = 'king'

class TeamType:
    OPPONENT = TeamTypeManager_.opponent
    OUR = TeamTypeManager_.our
    DRAW = 'd'