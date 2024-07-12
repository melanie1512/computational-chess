from ..models.Types import PieceType, TeamType
from ..models.Board import Board
from ..models.Piece import Piece
from ..models.Position import Position
from ..db.database import db
from sqlalchemy.orm import sessionmaker, make_transient, object_session
import requests
import copy

def get_board_state(board_id):
    url = f"http://127.0.0.1:5000/show_board/{board_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to get board state. Status code: {response.status_code}")
        return None

def reattach_to_session(instance, session):
    previous_session = object_session(instance)
    if previous_session:
        previous_session.expunge(instance)
    
    make_transient(instance)
    
    if hasattr(instance, 'position') and instance.position:
        previous_position_session = object_session(instance.position)
        if previous_position_session:
            previous_position_session.expunge(instance.position)
        make_transient(instance.position)
        instance.position = session.merge(instance.position)
    
    instance = session.merge(instance)
    session.flush()  # Optional, ensures the instance is properly added to the session
    return instance



def play_move_wrapper_sim(board, move, session):
    valid_move = True
    played_piece = move['played_piece']
    destination = move['destination']
    
    if isinstance(destination, dict):
        destination = Position.from_dict(destination)
    
    # Reattach to session
    played_piece = reattach_to_session(played_piece, session)
    destination = reattach_to_session(destination, session)

    board.play_move(False, valid_move, played_piece, destination)

    print("Simulated board state after move:")
    print(board.to_dict())
    return

def play_move_wrapper(board, move):
    valid_move = True
    played_piece = move['played_piece']
    destination = move['destination']
    
    if isinstance(destination, dict):
        destination = Position.from_dict(destination)
    
    board.play_move(False, valid_move, played_piece, destination)
    print(move)
    db.session.commit()

    print("Board state after move:")
    print(get_board_state(1))
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

def get_session():
    # Ensure this is called within the application context
    Session = sessionmaker(bind=db.engine)
    return Session()

def clone_board(original_board, session):
    new_board = Board(total_turns=original_board.total_turns)
    session.add(new_board)
    session.flush()  # Ensure the new board gets an id

    piece_mapping = {}  # Keep track of old to new piece mapping
    position_mapping = {}  # Keep track of old to new position mapping

    for piece in original_board.pieces:
        new_position = Position(x=piece.position.x, y=piece.position.y)
        session.add(new_position)
        session.flush()  # Ensure the new position gets an id
        position_mapping[piece.position.id] = new_position.id

        new_piece = Piece(
            image=piece.image,
            position_id=new_position.id,
            type=piece.type,
            team=piece.team,
            has_moved=piece.has_moved,
            is_checked=piece.is_checked,
            possible_moves=piece.possible_moves,
            board_id=new_board.id
        )
        session.add(new_piece)
        session.flush()  # Ensure the new piece gets an id
        piece_mapping[piece.id] = new_piece.id

    session.flush()  # Ensure all pieces and positions are added
    return new_board


# def minimax(board, depth, alpha, beta, maximizing_player):
#     if depth == 0 or board.is_game_over():
#         return evaluate_board(board), None

#     best_move = None

#     if maximizing_player:
#         max_eval = float('-inf')
#         for move in board.get_all_possible_moves(TeamType.OUR):
#             new_session = get_session()
#             simulated_board = clone_board(board, new_session)
#             play_move_wrapper_sim(simulated_board, move, new_session)
#             eval, _ = minimax(simulated_board, depth - 1, alpha, beta, False)
#             new_session.close()
#             if eval > max_eval:
#                 max_eval = eval
#                 best_move = move
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#         return max_eval, best_move
#     else:
#         min_eval = float('inf')
#         for move in board.get_all_possible_moves(TeamType.OPPONENT):
#             new_session = get_session()
#             simulated_board = clone_board(board, new_session)
#             play_move_wrapper_sim(simulated_board, move, new_session)
#             eval, _ = minimax(simulated_board, depth - 1, alpha, beta, True)
#             new_session.close()
#             if eval < min_eval:
#                 min_eval = eval
#                 best_move = move
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#         return min_eval, best_move

def minimax(board, depth, alpha, beta, maximizing_player, session):

    if depth == 0 or board.is_game_over():
        return board.evaluate(), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in board.get_all_possible_moves(TeamType.OUR):
            simulated_board = clone_board(board, session)
            play_move_wrapper_sim(simulated_board, move, session)
            eval, _ = minimax(simulated_board, depth - 1, alpha, beta, False, session)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in board.get_all_possible_moves(TeamType.OPPONENT):
            simulated_board = clone_board(board, session)
            play_move_wrapper_sim(simulated_board, move, session)
            eval, _ = minimax(simulated_board, depth - 1, alpha, beta, True, session)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move
