from ..models.Types import PieceType, TeamType
from ..models.Board import Board
from ..models.Position import Position

def play_move_wrapper(board, move):
    valid_move = True
    played_piece = move['played_piece']
    destination = move['destination']
    
    if isinstance(destination, dict):
        destination = Position.from_dict(destination)

    played_piece = next(piece for piece in board.pieces if piece.id == played_piece.id)

    board.play_move(False, valid_move, played_piece, destination)
    print("Board state after move:", board.to_dict())
    return


def evaluate_board(board):
    piece_values = {
        PieceType.PAWN: 10,
        PieceType.KNIGHT: 30,
        PieceType.BISHOP: 30,
        PieceType.ROOK: 50,
        PieceType.QUEEN: 90,
        PieceType.KING: 900
    }

    score = 0
    for piece in board.pieces:
        value = piece_values[piece.type]
        if piece.team == TeamType.OUR:
            score += value
        else:
            score -= value

    return score

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.get_all_possible_moves(TeamType.OUR):
            simulated_board = board.clone()
            play_move_wrapper(simulated_board, move)
            eval, _ = minimax(simulated_board, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in board.get_all_possible_moves(TeamType.OPPONENT):
            simulated_board = board.clone()
            play_move_wrapper(simulated_board, move)
            eval, _ = minimax(simulated_board, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move