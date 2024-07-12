import math
from .Board import Board
from .Types import TeamType
from .Position import Position
import random
from app.models.Piece import get_piece_


def minimax(board_: Board, depth: int, maximizing_player: int, alpha: int, beta: int, data: list, save_data: bool = False):
    if depth == 0 or board_.winning_team != None:    
        return board_.evaluate(), None
    valid_move = True
    if maximizing_player:
        max_eval = -math.inf

        for piece in board_.get_pieces():
            p = get_piece_(piece.get_id())
            p = p.clone()
            if p.get_team() == TeamType.OPPONENT:
                for move in p.get_possible_moves():
                    prev_pos = p.get_position()
                    m = Position(move['x'], move['y'])
                    _, _piece = board_.play_move(False, valid_move, p, m)
                    eval = minimax(board_, depth - 1, False, alpha, beta, data, False)[0]
                    #falta recolocar la pieza eliminada
                    board_.undo_move(p, prev_pos, _piece)
                    if save_data:
                        if eval >= max_eval:
                            if eval > data[0]:
                                data[0] = eval
                                data[1] = [[move, piece.get_id(), eval, piece.type]]
                            elif eval == data[0]:
                                data[1].append([move, piece.get_id(), eval, piece.type])
                        max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return data
    else:
        min_eval = math.inf
        for piece in board_.get_pieces():
            p = get_piece_(piece.get_id())
            p = p.clone()
            if p.get_team() == TeamType.OUR:
                for move in p.get_possible_moves():
                    prev_pos = p.get_position()
                    m = Position(move['x'], move['y'])
                    _, _piece = board_.play_move(False, valid_move, p, m)
                    eval = minimax(board_, depth - 1, True, alpha, beta, data, False)[0]
                    board_.undo_move(p, prev_pos, _piece)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return data
    

def ai_move(board: Board, depth: int):
    data = [0, []]
    board_ = board.clone()
    data = minimax(board_, depth, True, -math.inf, math.inf, data, True)
    print(data)
    if len(data[1]) == 0:
        return None
    best_score = max(data[1], key=lambda x: x[2])[2]
    piece_and_move = random.choice([move for move in data[1] if move[2] == best_score])
    print(piece_and_move)
    piece = piece_and_move[1]
    move = piece_and_move[0]

    destination_piece = get_piece_(piece)
    m = Position(move['x'], move['y'])
    board.play_move(False, True, destination_piece, m)
    return True