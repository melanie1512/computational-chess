from backend.app.models.Board import Piece, Position, TeamType
from backend.app.models.Pawn import Pawn
from .GeneralRules import (
    tile_is_occupied,
    tile_is_occupied_by_opponent,
    tile_is_empty_or_occupied_by_opponent,
)


def pawn_move(initial_position, desired_position, team, board_state):
    from app.models import Position, TeamType, Pawn
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
    from app.models import Position, TeamType, Pawn

    possible_moves = []
    special_row = 1 if pawn.team == TeamType.OUR else 6
    pawn_direction = 1 if pawn.team == TeamType.OUR else -1

    def is_valid_position(x, y):
        return 1 <= x <= 8 and 1 <= y <= 8

    # Movimiento normal
    normal_x = pawn.position.x
    normal_y = pawn.position.y + pawn_direction
    if is_valid_position(normal_x, normal_y):
        normal_move = Position(normal_x, normal_y)
        if not tile_is_occupied(normal_move, board_state):
            possible_moves.append(normal_move)
            # Movimiento especial (doble)
            if pawn.position.y == special_row:
                special_y = normal_y + pawn_direction
                if is_valid_position(normal_x, special_y):
                    special_move = Position(normal_x, special_y)
                    if not tile_is_occupied(special_move, board_state):
                        possible_moves.append(special_move)

    # Ataques diagonales
    for dx in [-1, 1]:
        attack_x = pawn.position.x + dx
        attack_y = pawn.position.y + pawn_direction
        if is_valid_position(attack_x, attack_y):
            attack_move = Position(attack_x, attack_y)
            if tile_is_occupied_by_opponent(attack_move, board_state, pawn.team):
                possible_moves.append(attack_move)
            # Captura en passant
            elif not tile_is_occupied(attack_move, board_state):
                adjacent_position = Position(attack_x, pawn.position.y)
                adjacent_piece = next((p for p in board_state if p.position.same_position(adjacent_position)), None)
                if adjacent_piece and isinstance(adjacent_piece, Pawn) and adjacent_piece.en_passant:
                    possible_moves.append(attack_move)

    return possible_moves
