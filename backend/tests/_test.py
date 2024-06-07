import pytest
from app.models.models import Piece, Board, Position

def test_can_create_some_position():
    pos = Position(15,20)
    assert  pos is not None

def test_can_create_valid_position():
    detected = Position(1,9)
    try:
        assert detected.is_valid() == True
    except:
        False, "is an invalid position"
        

def test_can_create_invalid_position():
    pass


def test_can_create_a_piece():
    pass

def test_have_same_position():
    pass

def test_can_create_a_piece():
    pass