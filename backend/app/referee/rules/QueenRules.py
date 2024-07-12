from app.models.Board import Position, TeamType
from app.models.Piece import Piece
from app.models.Pawn import Pawn
from .GeneralRules import (
    tile_is_occupied,
    tile_is_occupied_by_opponent,
    tile_is_empty_or_occupied_by_opponent,
)
from typing import List


def queen_move(
    initial_position: Position,
    desired_position: Position,
    team: str,
    board_state: List[Piece],
) -> bool:
    for i in range(1, 8):
        # Diagonal
        multiplier_x = (
            -1
            if desired_position.x < initial_position.x
            else (1 if desired_position.x > initial_position.x else 0)
        )
        multiplier_y = (
            -1
            if desired_position.y < initial_position.y
            else (1 if desired_position.y > initial_position.y else 0)
        )

        passed_position = Position(
            initial_position.x + (i * multiplier_x),
            initial_position.y + (i * multiplier_y),
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


def get_possible_queen_moves(queen: Piece, board_state: List[Piece]):
    possible_moves: List[Position] = []

    directions = [
        (0, 1),  # Arriba
        (0, -1),  # Abajo
        (1, 0),  # Derecha
        (-1, 0),  # Izquierda
        (1, 1),  # Derecha Arriba
        (1, -1),  # Abajo Derecha
        (-1, 1),  # Arriba Izquierda
        (-1, -1),  # Abajo izquierda
    ]

    for dx, dy in directions:
        for i in range(1, 8):
            destination = Position(queen.position.x + i * dx, queen.position.y + i * dy)

            if not tile_is_occupied(destination, board_state) and destination.is_valid():
                possible_moves.append(destination.to_dict())
            elif tile_is_occupied_by_opponent(destination, board_state, queen.team) and destination.is_valid():
                possible_moves.append(destination.to_dict())
                break
            else:
                break

    return possible_moves
