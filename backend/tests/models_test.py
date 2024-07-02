import pytest
from app.models.Board import Board, Position, PieceType, TeamType
from app.models.Piece import Piece

# test Position


def test_can_create_some_position():
    pos = Position(x=1, y=8)
    assert pos is not None
    assert pos.x == 1
    assert pos.y == 8


def test_can_create_valid_position():
    try:
        pos = Position(x=1, y=8)
        assert pos is not None
    except Exception:
        pytest.fail("Failed to create a valid position")


def test_cannot_create_invalid_position():
    try:
        pos = Position(x=11, y=9)
        assert False, "Should not be able to create an invalid position"
    except ValueError as e:
        assert str(e) == "Invalid position coordinates"


def test_positions_are_equal():
    pos1 = Position(x=1, y=8)
    pos2 = Position(x=1, y=8)
    assert pos1.same_position(pos2)


def test_positions_are_not_equal():
    pos1 = Position(x=1, y=8)
    pos2 = Position(x=2, y=8)
    assert not pos1.same_position(pos2)


def test_position_is_valid():
    pos = Position(x=1, y=8)
    assert pos.is_valid()


def test_position_clone():
    pos1 = Position(x=1, y=2)
    pos2 = pos1.clone()

    assert pos1.x == pos2.x
    assert pos1.y == pos2.y


# test Piece


def test_piece_is_type():
    Piece1 = Piece(Position(x=1, y=8), PieceType.PAWN, TeamType.OUR)
    assert Piece1.is_pawn == True

    Piece2 = Piece(Position(x=1, y=8), PieceType.ROOK, TeamType.OUR)
    assert Piece2.is_rook == True

    Piece3 = Piece(Position(x=1, y=8), PieceType.KNIGHT, TeamType.OUR)
    assert Piece3.is_knight == True

    Piece4 = Piece(Position(x=1, y=8), PieceType.BISHOP, TeamType.OUR)
    assert Piece4.is_bishop == True

    Piece5 = Piece(Position(x=1, y=8), PieceType.KING, TeamType.OUR)
    assert Piece5.is_king == True

    Piece6 = Piece(Position(x=1, y=8), PieceType.QUEEN, TeamType.OUR)
    assert Piece6.is_queen == True


def test_piece_is_not_type():
    Piece1 = Piece(Position(x=1, y=8), PieceType.PAWN, TeamType.OUR)
    assert Piece1.is_rook == False

    Piece2 = Piece(Position(x=1, y=8), PieceType.ROOK, TeamType.OUR)
    assert Piece2.is_knight == False

    Piece3 = Piece(Position(x=1, y=8), PieceType.KNIGHT, TeamType.OUR)
    assert Piece3.is_bishop == False

    Piece4 = Piece(Position(x=1, y=8), PieceType.BISHOP, TeamType.OUR)
    assert Piece4.is_king == False

    Piece5 = Piece(Position(x=1, y=8), PieceType.KING, TeamType.OUR)
    assert Piece5.is_queen == False

    Piece6 = Piece(Position(x=1, y=8), PieceType.QUEEN, TeamType.OUR)
    assert Piece6.is_pawn == False


def test_same_piece_position():
    Piece1 = Piece(Position(x=1, y=8), PieceType.ROOK, TeamType.OUR)
    Piece2 = Piece(Position(x=1, y=8), PieceType.PAWN, TeamType.OUR)
    assert Piece1.same_piece_position(Piece2) == True


def test_different_piece_position():
    Piece1 = Piece(Position(x=5, y=8), PieceType.ROOK, TeamType.OUR)
    Piece2 = Piece(Position(x=1, y=8), PieceType.PAWN, TeamType.OUR)
    assert Piece1.same_piece_position(Piece2) == False


def test_piece_same_position():
    Pos1 = Position(x=1, y=8)
    Piece1 = Piece(Position(x=1, y=8), PieceType.ROOK, TeamType.OUR)
    assert Piece1.same_position(Pos1) == True


def test_piece_different_position():
    Pos1 = Position(x=1, y=8)
    Piece1 = Piece(Position(x=1, y=2), PieceType.ROOK, TeamType.OUR)
    assert Piece1.same_position(Pos1) == False


def test_piece_clone():
    Piece1 = Piece(Position(x=1, y=2), PieceType.ROOK, TeamType.OUR)
    Piece2 = Piece1.clone()

    assert Piece1.position.x == Piece2.position.x
    assert Piece1.position.y == Piece2.position.y
    assert Piece1.type == Piece2.type
    assert Piece1.team == Piece2.team
    assert Piece1.has_moved == Piece2.has_moved

    assert len(Piece1.possible_moves) == len(Piece2.possible_moves)
    for cp_move, op_move in zip(Piece2.possible_moves, Piece1.possible_moves):
        assert cp_move.same_position(op_move)


# test Board


def setup_board():
    # initializing pieces
    pieces = [
        Piece(Position(1, 1), PieceType.ROOK, TeamType.OUR),
        Piece(Position(2, 1), PieceType.KNIGHT, TeamType.OUR),
        Piece(Position(3, 1), PieceType.BISHOP, TeamType.OUR),
        Piece(Position(4, 1), PieceType.QUEEN, TeamType.OUR),
        Piece(Position(5, 1), PieceType.KING, TeamType.OUR),
        Piece(Position(6, 1), PieceType.BISHOP, TeamType.OUR),
        Piece(Position(7, 1), PieceType.KNIGHT, TeamType.OUR),
        Piece(Position(8, 1), PieceType.ROOK, TeamType.OUR),
        Piece(Position(1, 2), PieceType.PAWN, TeamType.OUR),
        Piece(Position(2, 2), PieceType.PAWN, TeamType.OUR),
        Piece(Position(3, 2), PieceType.PAWN, TeamType.OUR),
        Piece(Position(4, 2), PieceType.PAWN, TeamType.OUR),
        Piece(Position(5, 2), PieceType.PAWN, TeamType.OUR),
        Piece(Position(6, 2), PieceType.PAWN, TeamType.OUR),
        Piece(Position(7, 2), PieceType.PAWN, TeamType.OUR),
        Piece(Position(8, 2), PieceType.PAWN, TeamType.OUR),
        Piece(Position(1, 8), PieceType.ROOK, TeamType.OPPONENT),
        Piece(Position(2, 8), PieceType.KNIGHT, TeamType.OPPONENT),
        Piece(Position(3, 8), PieceType.BISHOP, TeamType.OPPONENT),
        Piece(Position(4, 8), PieceType.QUEEN, TeamType.OPPONENT),
        Piece(Position(5, 8), PieceType.KING, TeamType.OPPONENT),
        Piece(Position(6, 8), PieceType.BISHOP, TeamType.OPPONENT),
        Piece(Position(7, 8), PieceType.KNIGHT, TeamType.OPPONENT),
        Piece(Position(8, 8), PieceType.ROOK, TeamType.OPPONENT),
        Piece(Position(1, 7), PieceType.PAWN, TeamType.OPPONENT),
        Piece(Position(2, 7), PieceType.PAWN, TeamType.OPPONENT),
        Piece(Position(3, 7), PieceType.PAWN, TeamType.OPPONENT),
        Piece(Position(4, 7), PieceType.PAWN, TeamType.OPPONENT),
        Piece(Position(5, 7), PieceType.PAWN, TeamType.OPPONENT),
        Piece(Position(6, 7), PieceType.PAWN, TeamType.OPPONENT),
        Piece(Position(7, 7), PieceType.PAWN, TeamType.OPPONENT),
        Piece(Position(8, 7), PieceType.PAWN, TeamType.OPPONENT),
    ]
    return Board(pieces, total_turns=1)


def test_board_initial_setup():
    board = setup_board()
    assert board is not None
    assert len(board.pieces) == 32
    assert board.total_turns == 1
    assert board.winning_team is None


def test_board_current_team():
    board = setup_board()
    assert board.current_team == TeamType.OUR
    board.total_turns += 1
    assert board.current_team == TeamType.OPPONENT


def test_board_get_valid_moves():
    board = setup_board()
    pawn = None
    for piece in board.pieces:
        if piece.is_pawn and piece.team == TeamType.OUR:
            pawn = piece
            break
    assert pawn is not None, "No se encontró un peón del equipo OUR"
    valid_moves = board.get_valid_moves(pawn, board.pieces)
    assert valid_moves is not None
    assert len(valid_moves) > 0
