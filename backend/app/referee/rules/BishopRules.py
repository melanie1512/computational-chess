from backend.app.models.models import Piece, Position, TeamType
from .GeneralRules import (
    tile_is_occupied,
    tile_is_occupied_by_opponent,
    tile_is_empty_or_occupied_by_opponent,
)
from typing import List


def bishop_move(initial_position, desired_position, team, board_state):
    for i in range(1, 8):
        # Movimiento a la derecha
        if (
            desired_position.x > initial_position.x
            and desired_position.y > initial_position.y
        ):
            passed_position = Position(initial_position.x + i, initial_position.y + i)
            # Chequear si el tile es tile final
            if passed_position.same_position(desired_position):
                # Mismo tile final
                if tile_is_empty_or_occupied_by_opponent(
                    passed_position, board_state, team
                ):
                    return True
            else:
                # Passing tile
                if tile_is_occupied(passed_position, board_state):
                    break

        # Movimiento bottom right
        if (
            desired_position.x > initial_position.x
            and desired_position.y < initial_position.y
        ):
            passed_position = Position(initial_position.x + i, initial_position.y - i)
            # Chequear si el tile es tile final
            if passed_position.same_position(desired_position):
                # Tile final
                if tile_is_empty_or_occupied_by_opponent(
                    passed_position, board_state, team
                ):
                    return True
            else:
                if tile_is_occupied(passed_position, board_state):
                    break

        # Movimiento bottom left
        if (
            desired_position.x < initial_position.x
            and desired_position.y < initial_position.y
        ):
            passed_position = Position(initial_position.x - i, initial_position.y - i)
            # Chequear si el tile es tile final
            if passed_position.same_position(desired_position):
                # Tile final
                if tile_is_empty_or_occupied_by_opponent(
                    passed_position, board_state, team
                ):
                    return True
            else:
                if tile_is_occupied(passed_position, board_state):
                    break

        # Movimiento top left
        if (
            desired_position.x < initial_position.x
            and desired_position.y > initial_position.y
        ):
            passed_position = Position(initial_position.x - i, initial_position.y + i)
            # Chequear si el tile es tile final
            if passed_position.same_position(desired_position):
                # Tile final
                if tile_is_empty_or_occupied_by_opponent(
                    passed_position, board_state, team
                ):
                    return True
            else:
                if tile_is_occupied(passed_position, board_state):
                    break
    return False


def get_possible_bishop_moves(bishop, boardstate):
    possible_moves: List[Position] = []

    # Movimiento upper right
    for i in range(1, 8):
        destination = Position(bishop.position.x + i, bishop.position.y + i)
        if not tile_is_occupied(destination, boardstate):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, boardstate, bishop.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Movimiento bottom right
    for i in range(1, 8):
        destination = Position(bishop.position.x + i, bishop.position.y - i)
        if not tile_is_occupied(destination, boardstate):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, boardstate, bishop.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Movimiento bottom left
    for i in range(1, 8):
        destination = Position(bishop.position.x - i, bishop.position.y - i)
        if not tile_is_occupied(destination, boardstate):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, boardstate, bishop.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Movimiento top left
    for i in range(1, 8):
        destination = Position(bishop.position.x - i, bishop.position.y + i)
        if not tile_is_occupied(destination, boardstate):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, boardstate, bishop.team):
            possible_moves.append(destination)
            break
        else:
            break

    return possible_moves
