import pytest
from app.models.models import Piece, Board, Position, PieceType, TeamType

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

# test Piece

def test_piece_is_type():
    Piece1 = Piece(Position(x=1, y=8), PieceType.PAWN,
                   TeamType.OUR)
    assert (Piece1.is_pawn == True)

    Piece2 = Piece(Position(x=1, y=8), PieceType.ROOK,
                   TeamType.OUR)
    assert (Piece2.is_rook == True)
    
    Piece3 = Piece(Position(x=1, y=8), PieceType.KNIGHT,
                   TeamType.OUR)
    assert (Piece3.is_knight == True)

    Piece4 = Piece(Position(x=1, y=8), PieceType.BISHOP,
                   TeamType.OUR)
    assert (Piece4.is_bishop == True)

    Piece5 = Piece(Position(x=1, y=8), PieceType.KING,
                   TeamType.OUR)
    assert (Piece5.is_king == True)

    Piece6 = Piece(Position(x=1, y=8), PieceType.QUEEN,
                   TeamType.OUR)
    assert (Piece6.is_queen == True)

def test_same_piece_position():
    Piece1 = Piece(Position(x=1, y=8), PieceType.ROOK,
                   TeamType.OUR)
    Piece2 = Piece(Position(x=1, y=8), PieceType.PAWN,
                   TeamType.OUR)
    assert (Piece1.same_piece_position(Piece2) == True)

def test_same_position():
    Pos1 = Position(x=1, y=8)
    Piece1 = Piece(Position(x=1, y=8), PieceType.ROOK,
                   TeamType.OUR)
    assert(Piece1.same_position(Pos1) == True)
    