import pytest
from app.models.models import Piece, Board, Position

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
