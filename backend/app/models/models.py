from ..database import db

from ..rules import (
    get_possible_pawn_moves,
    get_possible_knight_moves,
    get_possible_bishop_moves,
    get_possible_rook_moves,
    get_possible_queen_moves,
    get_possible_king_moves,
    get_castling_moves,
)


class Position(db.Model):
    __tablename__ = "positions"
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)

    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def same_position(self, other_position):
        return self.x == other_position.x and self.y == other_position.y

    def clone(self):
        return Position(x=self.x, y=self.y)


class Piece(db.Model):
    __tablename__ = "pieces"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey("positions.id"), nullable=False)
    position = db.relationship("Position", backref=db.backref("pieces", lazy=True))
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
            possible_moves=[pos.clone() for pos in self.possible_moves],
        )


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


# Board:


class Board:
    def __init__(self, pieces, total_turns):
        self.pieces = pieces
        self.total_turns = total_turns
        self.winning_team = None

    @property
    def current_team(self):
        return TeamType.OPPONENT if self.total_turns % 2 == 0 else TeamType.OUR

    def calculate_all_moves(self):
        for piece in self.pieces:
            piece.possible_moves = self.get_valid_moves(piece, self.pieces)
        for king in filter(lambda p: p.is_king, self.pieces):
            if king.possible_moves is not None:
                king.possible_moves.extend(get_castling_moves(king, self.pieces))
        self.check_current_team_moves()
        for piece in filter(lambda p: p.team != self.current_team, self.pieces):
            piece.possible_moves = []
        if not any(
            p.possible_moves
            for p in filter(lambda p: p.team == self.current_team, self.pieces)
        ):
            king = next(
                filter(lambda p: p.is_king and p.team == self.current_team, self.pieces)
            )
            self.winning_team = (
                TeamType.DRAW
                if not king.is_checked
                else (
                    TeamType.OPPONENT
                    if self.current_team == TeamType.OUR
                    else TeamType.OUR
                )
            )

    def check_current_team_moves(self):
        for piece in filter(lambda p: p.team == self.current_team, self.pieces):
            if piece.possible_moves is None:
                continue
            for move in piece.possible_moves:
                simulated_board = self.clone()
                simulated_board.pieces = [
                    p for p in simulated_board.pieces if not p.same_position(move)
                ]
                cloned_piece = next(
                    p for p in simulated_board.pieces if p.same_piece_position(piece)
                )
                cloned_piece.position = move.clone()
                cloned_king = next(
                    p
                    for p in simulated_board.pieces
                    if p.is_king and p.team == simulated_board.current_team
                )
                for enemy in filter(
                    lambda p: p.team != simulated_board.current_team,
                    simulated_board.pieces,
                ):
                    enemy.possible_moves = simulated_board.get_valid_moves(
                        enemy, simulated_board.pieces
                    )
                    if enemy.is_pawn and any(
                        m.x != enemy.position.x
                        and m.same_position(cloned_king.position)
                        for m in enemy.possible_moves
                    ):
                        piece.possible_moves = [
                            m for m in piece.possible_moves if not m.same_position(move)
                        ]
                    elif any(
                        m.same_position(cloned_king.position)
                        for m in enemy.possible_moves
                    ):
                        piece.possible_moves = [
                            m for m in piece.possible_moves if not m.same_position(move)
                        ]
            king = next(
                p for p in self.pieces if p.is_king and p.team == self.current_team
            )
            for enemy in filter(lambda p: p.team != self.current_team, self.pieces):
                enemy.possible_moves = self.get_valid_moves(enemy, self.pieces)
                if enemy.is_pawn and any(
                    m.x != enemy.position.x and m.same_position(king.position)
                    for m in enemy.possible_moves
                ):
                    king.is_checked = True
                elif any(m.same_position(king.position) for m in enemy.possible_moves):
                    king.is_checked = True

    def get_valid_moves(self, piece, board_state):
        if piece.type == PieceType.PAWN:
            return get_possible_pawn_moves(piece, board_state)
        elif piece.type == PieceType.KNIGHT:
            return get_possible_knight_moves(piece, board_state)
        elif piece.type == PieceType.BISHOP:
            return get_possible_bishop_moves(piece, board_state)
        elif piece.type == PieceType.ROOK:
            return get_possible_rook_moves(piece, board_state)
        elif piece.type == PieceType.QUEEN:
            return get_possible_queen_moves(piece, board_state)
        elif piece.type == PieceType.KING:
            return get_possible_king_moves(piece, board_state)
        else:
            return []

    def play_move(self, en_passant_move, valid_move, played_piece, destination):
        pawn_direction = 1 if played_piece.team == TeamType.OUR else -1
        destination_piece = next(
            (p for p in self.pieces if p.same_position(destination)), None
        )
        if (
            played_piece.is_king
            and destination_piece
            and destination_piece.is_rook
            and destination_piece.team == played_piece.team
        ):
            direction = (
                1 if destination_piece.position.x - played_piece.position.x > 0 else -1
            )
            new_king_x_position = played_piece.position.x + direction * 2
            for piece in self.pieces:
                if piece.same_piece_position(played_piece):
                    piece.position.x = new_king_x_position
                elif piece.same_piece_position(destination_piece):
                    piece.position.x = new_king_x_position - direction
            self.calculate_all_moves()
            return True
        if en_passant_move:
            self.pieces = [
                piece
                for piece in self.pieces
                if not (
                    piece.is_pawn
                    and piece.same_position(
                        Position(destination.x, destination.y - pawn_direction)
                    )
                )
            ]
            played_piece.position.x = destination.x
            played_piece.position.y = destination.y
            played_piece.has_moved = True
            self.calculate_all_moves()
        elif valid_move:
            self.pieces = [
                piece for piece in self.pieces if not piece.same_position(destination)
            ]
            played_piece.position.x = destination.x
            played_piece.position.y = destination.y
            played_piece.has_moved = True
            self.calculate_all_moves()
        else:
            return False
        return True

    def clone(self):
        return Board([piece.clone() for piece in self.pieces], self.total_turns)


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
