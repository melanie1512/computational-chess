from app.models.Board import Position, PieceType, TeamType, Board
from app.models.Piece import Piece

# Test Pawn


def test_pawn_moves_blocked():
    blocking_piece = Piece(Position(1, 3), PieceType.ROOK, TeamType.OUR)
    pawn = Piece(Position(1, 2), PieceType.PAWN, TeamType.OUR)
    board = Board([pawn, blocking_piece], 0)
    moves = board.get_valid_moves(pawn, board.pieces)
    assert all(not move.same_position(Position(1, 3)) for move in moves)
    assert all(not move.same_position(Position(1, 4)) for move in moves)


def test_pawn_edge_of_board():
    pawn = Piece(Position(1, 8), PieceType.PAWN, TeamType.OUR)
    board = Board([pawn], 0)
    moves = board.get_valid_moves(pawn, board.pieces)
    assert not moves


# def test_rook_moves_blocked():
#     blocking_piece = Piece(Position(1, 2), PieceType.PAWN, TeamType.OUR)
#     rook = Piece(Position(1, 1), PieceType.ROOK, TeamType.OUR)
#     board = Board([rook, blocking_piece], 0)
#     moves = board.get_valid_moves(rook, board.pieces)
#     assert all(not move.same_position(Position(1, 8)) for move in moves)


# def test_rook_edge_of_board():
#     rook = Piece(Position(8, 8), PieceType.ROOK, TeamType.OUR)
#     board = Board([rook], 0)
#     moves = board.get_valid_moves(rook, board.pieces)
#     assert any(move.same_position(Position(8, 1)) for move in moves)


def test_king_moves_blocked():
    blocking_piece = Piece(Position(5, 2), PieceType.PAWN, TeamType.OUR)
    king = Piece(Position(5, 1), PieceType.KING, TeamType.OUR)
    board = Board([king, blocking_piece], 0)
    moves = board.get_valid_moves(king, board.pieces)
    assert all(not move.same_position(Position(5, 2)) for move in moves)


def test_king_edge_of_board():
    king = Piece(Position(1, 1), PieceType.KING, TeamType.OUR)
    board = Board([king], 0)
    moves = board.get_valid_moves(king, board.pieces)
    assert any(move.same_position(Position(2, 1)) for move in moves)


# def test_bishop_moves_blocked():
#     blocking_piece = Piece(Position(4, 4), PieceType.PAWN, TeamType.OUR)
#     bishop = Piece(Position(3, 3), PieceType.BISHOP, TeamType.OUR)
#     board = Board([bishop, blocking_piece], 0)
#     moves = board.get_valid_moves(bishop, board.pieces)
#     assert all(not move.same_position(Position(5, 5)) for move in moves)


# def test_bishop_edge_of_board():
#     bishop = Piece(Position(8, 8), PieceType.BISHOP, TeamType.OUR)
#     board = Board([bishop], 0)
#     moves = board.get_valid_moves(bishop, board.pieces)
#     assert any(move.same_position(Position(1, 1)) for move in moves)


# def test_no_overlap_after_move():
#     pawn1 = Piece(Position(1, 2), PieceType.PAWN, TeamType.OUR)
#     pawn2 = Piece(Position(1, 4), PieceType.PAWN, TeamType.OUR)
#     board = Board([pawn1, pawn2], 0)
#     moves = board.get_valid_moves(pawn1, board.pieces)
#     assert all(not move.same_position(Position(1, 4)) for move in moves)


# def test_stay_within_board():
#     rook = Piece(Position(8, 1), PieceType.ROOK, TeamType.OUR)
#     board = Board([rook], 0)
#     moves = board.get_valid_moves(rook, board.pieces)
#     assert all(1 <= move.x <= 8 and 1 <= move.y <= 8 for move in moves)
