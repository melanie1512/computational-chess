from backend.app.models.models import Piece, Position, TeamType, Pawn
from .GeneralRules import (
    tile_is_occupied,
    tile_is_occupied_by_opponent,
    tile_is_empty_or_occupied_by_opponent,
)
from typing import List


def knight_move(
    initial_position: Position,
    desired_position: Position,
    team: TeamType,
    board_state: List[Piece],
):
    for i in range(-1, 2, 2):
        for j in range(-1, 2, 2):
            # Movimiento hacia arriba y abajo
            if desired_position.y - initial_position.y == 2 * i:
                if desired_position.x - initial_position.x == j:
                    if tile_is_empty_or_occupied_by_opponent(
                        desired_position, board_state, team
                    ):
                        return True

            # Movimiento hacia derecha e izquierda
            if desired_position.x - initial_position.x == 2 * i:
                if desired_position.y - initial_position.y == j:
                    if tile_is_empty_or_occupied_by_opponent(
                        desired_position, board_state, team
                    ):
                        return True
    return False


def get_possible_knight_moves(knight: Piece, board_state: List[Piece]):
    possible_moves: List[Position] = []

    for i in range(-1, 2, 2):
        for j in range(-1, 2, 2):
            vertical_move = Position(knight.position.x + j, knight.position.y + i * 2)
            horizontal_move = Position(knight.position.x + i * 2, knight.position.y + j)

            if tile_is_empty_or_occupied_by_opponent(
                vertical_move, board_state, knight.team
            ):
                possible_moves.append(vertical_move)

            if tile_is_empty_or_occupied_by_opponent(
                horizontal_move, board_state, knight.team
            ):
                possible_moves.append(horizontal_move)

    return possible_moves
