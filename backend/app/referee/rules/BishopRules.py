from app.models.Board import TeamType
from app.models.Piece import Piece, Position
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


def get_possible_bishop_moves(bishop, board_state):
    possible_moves = []

    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def is_valid_position(x, y):
        return 0 <= x < 8 and 0 <= y < 8

    for dx, dy in directions:
        for i in range(1, 8):
            destination_x = bishop.position.x + i * dx
            destination_y = bishop.position.y + i * dy
            if not is_valid_position(destination_x, destination_y):
                break
            destination = Position(destination_x, destination_y)
            if not tile_is_occupied(destination, board_state):
                possible_moves.append(destination.to_dict())
            elif tile_is_occupied_by_opponent(destination, board_state, bishop.team):
                possible_moves.append(destination.to_dict())
                break
            else:
                break

    return possible_moves

"""
def get_possible_bishop_moves(bishop, boardstate):
    possible_moves: List[Position] = []

    # Movimiento upper right
    for i in range(1, 8):
        destination = Position(bishop.position.x + i, bishop.position.y + i)
        if not tile_is_occupied(destination, boardstate):
            possible_moves.append(destination.to_dict())
        elif tile_is_occupied_by_opponent(destination, boardstate, bishop.team):
            possible_moves.append(destination.to_dict())
            break
        else:
            break

    # Movimiento bottom right
    for i in range(1, 8):
        destination = Position(bishop.position.x + i, bishop.position.y - i)
        if not tile_is_occupied(destination, boardstate):
            possible_moves.append(destination.to_dict())
        elif tile_is_occupied_by_opponent(destination, boardstate, bishop.team):
            possible_moves.append(destination.to_dict())
            break
        else:
            break

    # Movimiento bottom left
    for i in range(1, 8):
        destination = Position(bishop.position.x - i, bishop.position.y - i)
        if not tile_is_occupied(destination, boardstate):
            possible_moves.append(destination.to_dict())
        elif tile_is_occupied_by_opponent(destination, boardstate, bishop.team):
            possible_moves.append(destination.to_dict())
            break
        else:
            break

    # Movimiento top left
    for i in range(1, 8):
        destination = Position(bishop.position.x - i, bishop.position.y + i)
        if not tile_is_occupied(destination, boardstate):
            possible_moves.append(destination.to_dict())
        elif tile_is_occupied_by_opponent(destination, boardstate, bishop.team):
            possible_moves.append(destination.to_dict())
            break
        else:
            break

    return possible_moves
"""