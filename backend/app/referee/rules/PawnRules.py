from app.models.Board import Position, TeamType
from app.models.Piece import Piece
from app.models.Pawn import Pawn
from .GeneralRules import (
    tile_is_occupied,
    tile_is_occupied_by_opponent,
    tile_is_empty_or_occupied_by_opponent,
)


def pawn_move(initial_position, desired_position, team, board_state):
    special_row = 1 if team == TeamType.OUR else 6
    pawn_direction = 1 if team == TeamType.OUR else -1

    # Movimiento doble desde la fila especial
    if (
        initial_position.x == desired_position.x
        and initial_position.y == special_row
        and desired_position.y - initial_position.y == 2 * pawn_direction
    ):
        if not tile_is_occupied(desired_position, board_state) and not tile_is_occupied(
            Position(desired_position.x, desired_position.y - pawn_direction),
            board_state,
        ):
            return True

    # Movimiento normal hacia adelante
    elif (
        initial_position.x == desired_position.x
        and desired_position.y - initial_position.y == pawn_direction
    ):
        if not tile_is_occupied(desired_position, board_state):
            return True

    # Captura en la esquina izquierda
    elif (
        desired_position.x - initial_position.x == -1
        and desired_position.y - initial_position.y == pawn_direction
    ):
        if tile_is_occupied_by_opponent(desired_position, board_state, team):
            return True

    # Captura en la esquina derecha
    elif (
        desired_position.x - initial_position.x == 1
        and desired_position.y - initial_position.y == pawn_direction
    ):
        if tile_is_occupied_by_opponent(desired_position, board_state, team):
            return True

    return False


def get_possible_pawn_moves(pawn, board_state):
    possible_moves = []
    special_row = 1 if pawn.team == TeamType.OUR else 6
    pawn_direction = 1 if pawn.team == TeamType.OUR else -1
    
    normal_move = Position(pawn.position.x, pawn.position.y + pawn_direction)
    special_move = Position(normal_move.x, normal_move.y + pawn_direction)
    upper_left_attack = Position(pawn.position.x - 1, pawn.position.y + pawn_direction)
    upper_right_attack = Position(pawn.position.x + 1, pawn.position.y + pawn_direction)
    left_position = Position(pawn.position.x - 1, pawn.position.y)
    right_position = Position(pawn.position.x + 1, pawn.position.y)
    
    if normal_move.is_valid():
        if not tile_is_occupied(normal_move, board_state):
            possible_moves.append(normal_move.to_dict())
            if pawn.position.y == special_row and not tile_is_occupied(
                special_move, board_state
            ):
                possible_moves.append(special_move.to_dict())

    if upper_left_attack.is_valid():
        if tile_is_occupied_by_opponent(upper_left_attack, board_state, pawn.team):
            possible_moves.append(upper_left_attack.to_dict())
        elif not tile_is_occupied(upper_left_attack, board_state):
            left_piece = next(
                (p for p in board_state if p.position.same_position(left_position)), None
            )
            if left_piece and isinstance(left_piece, Pawn) and left_piece.en_passant:
                possible_moves.append(upper_left_attack.to_dict())

    if upper_right_attack.is_valid():
        if tile_is_occupied_by_opponent(upper_right_attack, board_state, pawn.team):
            possible_moves.append(upper_right_attack.to_dict())
        elif not tile_is_occupied(upper_right_attack, board_state):
            right_piece = next(
                (p for p in board_state if p.position.same_position(right_position)), None
            )
            if right_piece and isinstance(right_piece, Pawn) and right_piece.en_passant:
                possible_moves.append(upper_right_attack.to_dict())

    return possible_moves