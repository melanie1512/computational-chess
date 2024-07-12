import math
from Board import Board
from Types import TeamType
import random


def minimax(board: Board, depth: int, maximizing_player: int):
    if depth == 0 or board.winning_team != None:    
        return board.evaluate(), None
    board_ = board.clone()

    if maximizing_player:
        max_eval = -math.inf
        best_move = None
        for piece in board.get_pieces():
            if piece.get_team() == TeamType.OPPONENT:
                for move in piece.get_possible_moves():
                    board_.move_piece(piece, move)
                    eval = minimax(board_, depth - 1, False)[0]
                    board_.undo_move()
                    if eval > max_eval:
                        max_eval = eval
                        best_move = move