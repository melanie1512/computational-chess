class TeamTypeManager:
    def __init__(self, our):
        self._our = 1 if our == "w" else 2
        self._opponent = 2 if our == "w" else 1

    @property
    def our(self):
        return self._our

    @our.setter
    def our(self, value):
        self._our = 1 if value == "w" else 2

    @property
    def opponent(self):
        return self._opponent

    @opponent.setter
    def opponent(self, value):
        self._opponent = 2 if value == "w" else 1


TeamTypeManager_ = TeamTypeManager("w")


class PieceType:
    PAWN = "pawn"
    BISHOP = "bishop"
    KNIGHT = "knight"
    ROOK = "rook"
    QUEEN = "queen"
    KING = "king"


class TeamType:
    OPPONENT = TeamTypeManager_.opponent
    OUR = TeamTypeManager_.our
    DRAW = "d"
