import pytest
from app.models import Piece, Position, PieceType, TeamType

# Test Pawn

def test_pawn_moves_blocked():
    blocking_piece = Piece(Position(1, 3), PieceType.ROOK, TeamType.OUR)
    pawn = Piece(Position(1, 2), PieceType.PAWN, TeamType.OUR)
    moves = pawn.get_valid_moves([blocking_piece])
    assert all(not move.same_position(Position(1, 4)) for move in moves)
    assert all(not move.same_position(Position(1, 3)) for move in moves)

def test_pawn_edge_of_board():
    pawn = Piece(Position(1, 8), PieceType.PAWN, TeamType.OUR)
    moves = pawn.get_valid_moves([])
    assert not moves

# Test Rook

def test_rook_moves_blocked():
    blocking_piece = Piece(Position(1, 2), PieceType.PAWN, TeamType.OUR)
    rook = Piece(Position(1, 1), PieceType.ROOK, TeamType.OUR)
    moves = rook.get_valid_moves([blocking_piece])
    assert all(not move.same_position(Position(1, 8)) for move in moves)

def test_rook_edge_of_board():
    rook = Piece(Position(8, 8), PieceType.ROOK, TeamType.OUR)
    moves = rook.get_valid_moves([])
    assert any(move.same_position(Position(8, 1)) for move in moves)

# Test King

def test_king_moves_blocked():
    blocking_piece = Piece(Position(5, 2), PieceType.PAWN, TeamType.OUR)
    king = Piece(Position(5, 1), PieceType.KING, TeamType.OUR)
    moves = king.get_valid_moves([blocking_piece])
    assert all(not move.same_position(Position(5, 2)) for move in moves)

def test_king_edge_of_board():
    king = Piece(Position(1, 1), PieceType.KING, TeamType.OUR)
    moves = king.get_valid_moves([])
    assert any(move.same_position(Position(2, 1)) for move in moves)

# Test Bishop

def test_bishop_moves_blocked():
    blocking_piece = Piece(Position(4, 4), PieceType.PAWN, TeamType.OUR)
    bishop = Piece(Position(3, 3), PieceType.BISHOP, TeamType.OUR)
    moves = bishop.get_valid_moves([blocking_piece])
    assert all(not move.same_position(Position(5, 5)) for move in moves)

def test_bishop_edge_of_board():
    bishop = Piece(Position(8, 8), PieceType.BISHOP, TeamType.OUR)
    moves = bishop.get_valid_moves([])
    assert any(move.same_position(Position(1, 1)) for move in moves)

# Test General Movement Constraints

def test_no_overlap_after_move():
    pawn1 = Piece(Position(1, 2), PieceType.PAWN, TeamType.OUR)
    pawn2 = Piece(Position(1, 4), PieceType.PAWN, TeamType.OUR)
    moves = pawn1.get_valid_moves([pawn2])
    assert all(not move.same_position(Position(1, 4)) for move in moves)

def test_stay_within_board():
    rook = Piece(Position(8, 1), PieceType.ROOK, TeamType.OUR)
    moves = rook.get_valid_moves([])
    assert all(1 <= move.x <= 8 and 1 <= move.y <= 8 for move in moves)
