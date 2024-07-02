from app.models.Piece import Piece
from app.models.Types import PieceType
# Pawn


class Pawn(Piece):
    def __init__(self, position, team, has_moved, en_passant=None, possible_moves=None):
        super().__init__(
            position, PieceType.PAWN, team, has_moved, possible_moves or []
        )
        self.en_passant = en_passant

    def clone(self):
        return Pawn(
            self.position.clone(),
            self.team,
            self.has_moved,
            self.en_passant,
            [m.clone() for m in (self.possible_moves or [])],
        )
