
from .GeneralRules import (
    tile_is_occupied,
    tile_is_occupied_by_opponent,
    tile_is_empty_or_occupied_by_opponent,
)
from typing import List


def rook_move(
    initial_position,
    desired_position,
    team,
    board_state,
):
    from app.models import  Position
    if initial_position.x == desired_position.x:
        for i in range(1, 8):
            multiplier = -1 if desired_position.y < initial_position.y else 1
            passed_position = Position(
                initial_position.x, initial_position.y + (i * multiplier)
            )

            if passed_position.same_position(desired_position):
                if tile_is_empty_or_occupied_by_opponent(
                    passed_position, board_state, team
                ):
                    return True
            else:
                if tile_is_occupied(passed_position, board_state):
                    break

    if initial_position.y == desired_position.y:
        for i in range(1, 8):
            multiplier = -1 if desired_position.x < initial_position.x else 1
            passed_position = Position(
                initial_position.x + (i * multiplier), initial_position.y
            )

            if passed_position.same_position(desired_position):
                if tile_is_empty_or_occupied_by_opponent(
                    passed_position, board_state, team
                ):
                    return True
            else:
                if tile_is_occupied(passed_position, board_state):
                    break

    return False

def get_possible_rook_moves(rook, board_state):
    from app.models import Position
    possible_moves = []

    # Movimiento arriba
    for i in range(1, 8):
        if rook.position.y + i > 8:
            break
        destination = Position(rook.position.x, rook.position.y + i)
        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, rook.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Movimiento abajo
    for i in range(1, 8):
        if rook.position.y - i < 1:
            break
        destination = Position(rook.position.x, rook.position.y - i)
        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, rook.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Movimiento izquierda
    for i in range(1, 8):
        if rook.position.x - i < 1:
            break
        destination = Position(rook.position.x - i, rook.position.y)
        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, rook.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Movimiento derecha
    for i in range(1, 8):
        if rook.position.x + i > 8:
            break
        destination = Position(rook.position.x + i, rook.position.y)
        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, rook.team):
            possible_moves.append(destination)
            break
        else:
            break

    return possible_moves
