from app.models.Types import PieceType, TeamType
from app.models.Position import Position
from app.db.database import db

from app.referee.rules.index import (
    get_possible_pawn_moves,
    get_possible_knight_moves,
    get_possible_bishop_moves,
    get_possible_rook_moves,
    get_possible_queen_moves,
    get_possible_king_moves,
    get_castling_moves,
)

from sqlalchemy.ext.declarative import declared_attr


class ModelMixin:
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# Board:
class Board(db.Model, ModelMixin):
    __tablename__ = "board"

    id = db.Column(db.Integer, primary_key=True)
    pieces = db.relationship(
        "Piece", backref="board", lazy=True, cascade="all, delete-orphan"
    )
    total_turns = db.Column(db.Integer, nullable=False, default=0)
    winning_team = db.Column(db.String, nullable=True)

    def __init__(self, pieces, total_turns):
        if pieces is None:
            self.pieces = []
        self.pieces = pieces
        self.total_turns = total_turns
        self.winning_team = None

    @property
    def current_team(self):
        return (
            TeamType.OPPONENT if self.total_turns % 2 == 0 else TeamType.OUR
        )  # se puede cambiar para modificar color de pieza

    def calculate_all_moves(self):
        try:
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
                    filter(
                        lambda p: p.is_king and p.team == self.current_team, self.pieces
                    )
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
        except Exception as e:
            print(f"Error during calculate_all_moves: {e}")
            raise

    def check_current_team_moves(self):
        for piece in filter(lambda p: p.team == self.current_team, self.pieces):
            if piece.possible_moves is None:
                continue
            for move_dict in piece.possible_moves:
                move = Position.from_dict(
                    move_dict
                )  # Convert dictionary back to Position object
                simulated_board = self.clone()
                simulated_board.pieces = [
                    p for p in simulated_board.pieces if not p.same_position(move)
                ]
                cloned_piece = next(
                    p for p in simulated_board.pieces if p.same_piece_position(piece)
                )
                cloned_piece.position = move.clone()  # Use the clone method
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
                        Position.from_dict(m).x != enemy.position.x
                        and Position.from_dict(m).same_position(cloned_king.position)
                        for m in enemy.possible_moves
                    ):
                        piece.possible_moves = [
                            m
                            for m in piece.possible_moves
                            if not Position.from_dict(m).same_position(move)
                        ]
                    elif any(
                        Position.from_dict(m).same_position(cloned_king.position)
                        for m in enemy.possible_moves
                    ):
                        piece.possible_moves = [
                            m
                            for m in piece.possible_moves
                            if not Position.from_dict(m).same_position(move)
                        ]
            king = next(
                p for p in self.pieces if p.is_king and p.team == self.current_team
            )
            for enemy in filter(lambda p: p.team != self.current_team, self.pieces):
                enemy.possible_moves = self.get_valid_moves(enemy, self.pieces)

                if enemy.is_pawn and any(
                    m["x"] != enemy.position.x
                    and Position.from_dict(m).same_position(king.position)
                    for m in enemy.possible_moves
                ):
                    king.is_checked = True
                elif any(
                    Position.from_dict(m).same_position(king.position)
                    for m in enemy.possible_moves
                ):
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
