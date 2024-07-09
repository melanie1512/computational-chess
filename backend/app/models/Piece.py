from ..db.database import db
from .Types import PieceType, TeamType
from .Position import Position
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.postgresql import JSON


class ModelMixin:
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Piece(db.Model, ModelMixin):
    __tablename__ = "pieces"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey("positions.id"), nullable=False)
    position = db.relationship("Position", backref=db.backref("pieces", lazy=True))
    type = db.Column(db.String, nullable=False)
    team = db.Column(db.Integer, nullable=False)
    has_moved = db.Column(db.Boolean, default=False)
    is_checked = db.Column(db.Boolean, default=False)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"), nullable=False)
    possible_moves = db.Column(MutableList.as_mutable(JSON), default=[])

    def __init__(
        self,
        position_id,
        type: PieceType,
        team: TeamType,
        has_moved=False,
        possible_moves=None,
    ):
        if possible_moves is None:
            possible_moves = []
        self.image = f'assets/images/{type}_{"w" if team == 1 else "b"}.png'
        self.position_id = position_id
        self.position = Position.query.get(position_id)
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
        return self.position.same_position(other_piece.position) if self.position and other_piece.position else False

    def same_position(self, other_position):
        return (
            self.position and 
            other_position and 
            self.position.x == other_position.x and 
            self.position.y == other_position.y
        )

    def clone(self):
        return Piece(
            position_id=self.position_id,
            type=self.type,
            team=self.team,
            has_moved=self.has_moved,
            possible_moves=[
                pos.to_dict() if isinstance(pos, Position) else pos for pos in self.possible_moves
            ],
        )


    def to_char(self):
        if self.team == 1:
            if self.is_pawn:
                return "♙"
            elif self.is_knight:
                return "♘"
            elif self.is_bishop:
                return "♗"
            elif self.is_rook:
                return "♖"
            elif self.is_queen:
                return "♕"
            elif self.is_king:
                return "♔"
        else:
            if self.is_pawn:
                return "♟︎"
            elif self.is_knight:
                return "♞"
            elif self.is_bishop:
                return "♝"
            elif self.is_rook:
                return "♜"
            elif self.is_queen:
                return "♛"
            elif self.is_king:
                return "♚"
