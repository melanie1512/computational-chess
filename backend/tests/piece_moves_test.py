from app.models.Piece import Piece, Position, PieceType, TeamType
from app.models.Board import Board

# Importamos las funciones de movimiento que hemos implementado

from app.referee.rules.BishopRules import bishop_move

from app.referee.rules.PawnRules import pawn_move

from app.referee.rules.KingRules import king_move

from app.referee.rules.KnightRules import knight_move

from app.referee.rules.QueenRules import queen_move

from app.referee.rules.RookRules import rook_move


# Tests para Bishop
def test_bishop_valid_move():
    bishop = Piece(Position(3, 3), PieceType.BISHOP, TeamType.OUR)
    board = Board([bishop], 0)
    assert bishop_move(Position(3, 3), Position(5, 5), TeamType.OUR, board.pieces) == True

def test_bishop_blocked_move():
    blocking_piece = Piece(Position(4, 4), PieceType.PAWN, TeamType.OUR)
    bishop = Piece(Position(3, 3), PieceType.BISHOP, TeamType.OUR)
    board = Board([bishop, blocking_piece], 0)
    assert bishop_move(Position(3, 3), Position(5, 5), TeamType.OUR, board.pieces) == False

# Tests para King
def test_king_valid_move():
    king = Piece(Position(5, 1), PieceType.KING, TeamType.OUR)
    board = Board([king], 0)
    assert king_move(Position(5, 1), Position(5, 2), TeamType.OUR, board.pieces) == True

def test_king_invalid_move():
    king = Piece(Position(5, 1), PieceType.KING, TeamType.OUR)
    board = Board([king], 0)
    assert king_move(Position(5, 1), Position(5, 3), TeamType.OUR, board.pieces) == False

# Tests para Knight
def test_knight_valid_move():
    knight = Piece(Position(3, 3), PieceType.KNIGHT, TeamType.OUR)
    board = Board([knight], 0)
    assert knight_move(Position(3, 3), Position(5, 4), TeamType.OUR, board.pieces) == True

def test_knight_invalid_move():
    knight = Piece(Position(3, 3), PieceType.KNIGHT, TeamType.OUR)
    board = Board([knight], 0)
    assert knight_move(Position(3, 3), Position(4, 4), TeamType.OUR, board.pieces) == False

# Tests para Pawn
def test_pawn_valid_move():
    pawn = Piece(Position(1, 2), PieceType.PAWN, TeamType.OUR)
    board = Board([pawn], 0)
    assert pawn_move(Position(1, 2), Position(1, 3), TeamType.OUR, board.pieces) == True

def test_pawn_blocked_move():
    blocking_piece = Piece(Position(1, 3), PieceType.ROOK, TeamType.OUR)
    pawn = Piece(Position(1, 2), PieceType.PAWN, TeamType.OUR)
    board = Board([pawn, blocking_piece], 0)
    assert pawn_move(Position(1, 2), Position(1, 3), TeamType.OUR, board.pieces) == False

# Tests para Queen
def test_queen_valid_move():
    queen = Piece(Position(4, 4), PieceType.QUEEN, TeamType.OUR)
    board = Board([queen], 0)
    assert queen_move(Position(4, 4), Position(6, 6), TeamType.OUR, board.pieces) == True

def test_queen_blocked_move():
    blocking_piece = Piece(Position(5, 5), PieceType.PAWN, TeamType.OUR)
    queen = Piece(Position(4, 4), PieceType.QUEEN, TeamType.OUR)
    board = Board([queen, blocking_piece], 0)
    assert queen_move(Position(4, 4), Position(6, 6), TeamType.OUR, board.pieces) == False

# Tests para Rook
def test_rook_valid_move():
    rook = Piece(Position(1, 1), PieceType.ROOK, TeamType.OUR)
    board = Board([rook], 0)
    assert rook_move(Position(1, 1), Position(1, 8), TeamType.OUR, board.pieces) == True

def test_rook_blocked_move():
    blocking_piece = Piece(Position(1, 2), PieceType.PAWN, TeamType.OUR)
    rook = Piece(Position(1, 1), PieceType.ROOK, TeamType.OUR)
    board = Board([rook, blocking_piece], 0)
    assert rook_move(Position(1, 1), Position(1, 8), TeamType.OUR, board.pieces) == False

# Test que el movimiento no salga del tablero
def test_stay_within_board():
    rook = Piece(Position(8, 1), PieceType.ROOK, TeamType.OUR)
    board = Board([rook], 0)
    assert all(1 <= move.x <= 8 and 1 <= move.y <= 8 for move in board.get_valid_moves(rook, board.pieces))

# Test que no haya superposición después de mover
def test_no_overlap_after_move():
    pawn1 = Piece(Position(1, 2), PieceType.PAWN, TeamType.OUR)
    pawn2 = Piece(Position(1, 4), PieceType.PAWN, TeamType.OUR)
    board = Board([pawn1, pawn2], 0)
    assert all(not move.same_position(Position(1, 4)) for move in board.get_valid_moves(pawn1, board.pieces))
