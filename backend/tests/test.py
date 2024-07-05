from .models_test import *
from .piece_test import *
from .piece_moves_test import *
import pytest
from dotenv import load_dotenv
import os

load_dotenv()

from app import create_app
from app.db.database import setup_db


class Test:
    def setUp(self):
        self.app = create_app()
        self.path = os.getenv("SQLALCHEMY_DATABASE_URI")

    def test_all(self):
        test_pawn_moves_blocked()
        test_pawn_edge_of_board()
        test_rook_moves_blocked()
        test_rook_edge_of_board()
        test_king_moves_blocked()
        test_king_edge_of_board()
        test_bishop_moves_blocked()
        test_bishop_edge_of_board()
        test_no_overlap_after_move()
        test_stay_within_board()
        test_bishop_valid_move()
        test_bishop_blocked_move()
        test_king_valid_move()
        test_king_invalid_move()
        test_knight_valid_move()
        test_knight_invalid_move()
        test_pawn_valid_move()
        test_pawn_blocked_move()
        test_queen_valid_move()
        test_queen_blocked_move()
        test_rook_valid_move()
        test_rook_blocked_move()
        test_stay_within_board()
        test_no_overlap_after_move()
        test_can_create_some_position()
        test_can_create_valid_position()
        test_cannot_create_invalid_position()
        test_positions_are_equal()
        test_positions_are_not_equal()
        test_position_is_valid()
        test_position_clone()
        test_piece_is_type()
        test_piece_is_not_type()
        test_same_piece_position()
        test_different_piece_position()
        test_piece_same_position()
        test_piece_different_position()
        test_piece_clone()
        test_board_initial_setup()
        test_board_current_team()
        test_board_get_valid_moves()
        assert True


T = Test()


def testing_all():
    T.test_all()
    assert True
