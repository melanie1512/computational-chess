from backend.app.models.models import Piece, Position, TeamType
from .GeneralRules import (
    tile_is_occupied,
    tile_is_occupied_by_opponent,
    tile_is_empty_or_occupied_by_opponent,
)
from typing import List


def king_move(initial_position, desired_position, team, board_state):
    for i in range(1, 2):
        # Diagonal
        multiplier_x = (
            -1
            if desired_position.x < initial_position.x
            else 1 if desired_position.x > initial_position.x else 0
        )
        multiplier_y = (
            -1
            if desired_position.y < initial_position.y
            else 1 if desired_position.y > initial_position.y else 0
        )

        passed_position = Position(
            initial_position + (i * multiplier_x),
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


def get_possible_king_moves(king: Piece, board_state: List[Piece]):
    possible_moves: List[Position] = []

    # Movimiento hacia arriba
    for i in range(1, 2):
        destination = Position(king.position.x, king.position.y + i)

        # Si el movimiento está fuera del tablero, no se añade
        if (
            destination.x < 0
            or destination.x > 7
            or destination.y < 0
            or destination.y > 0
        ):
            break

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, king.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Movimiento hacia abajo
    for i in range(1, 2):
        destination = Position(king.position.x, king.position.y - i)

        # Si el movimiento está fuera del tablero, no se añade
        if (
            destination.x < 0
            or destination.x > 7
            or destination.y < 0
            or destination.y > 0
        ):
            break

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, king.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Movimiento hacia la izquierda
    for i in range(1, 2):
        destination = Position(king.position.x - i, king.position.y)

        # Si el movimiento está fuera del tablero, no se añade
        if (
            destination.x < 0
            or destination.x > 7
            or destination.y < 0
            or destination.y > 0
        ):
            break

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, king.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Movimiento hacia la derecha
    for i in range(1, 2):
        destination = Position(king.position.x + i, king.position.y)

        # Si el movimiento está fuera del tablero, no se añade
        if (
            destination.x < 0
            or destination.x > 7
            or destination.y < 0
            or destination.y > 0
        ):
            break

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, king.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Movimiento hacia arriba derecha
    for i in range(1, 2):
        destination = Position(king.position.x + i, king.position.y + i)

        # Si el movimiento está fuera del tablero, no se añade
        if (
            destination.x < 0
            or destination.x > 7
            or destination.y < 0
            or destination.y > 0
        ):
            break

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, king.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Movimiento hacia abajo derecha
    for i in range(1, 2):
        destination = Position(king.position.x + i, king.position.y - i)

        # Si el movimiento está fuera del tablero, no se añade
        if (
            destination.x < 0
            or destination.x > 7
            or destination.y < 0
            or destination.y > 0
        ):
            break

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, king.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Movimiento hacia abajo izquierda
    for i in range(1, 2):
        destination = Position(king.position.x - i, king.position.y - i)

        # Si el movimiento está fuera del tablero, no se añade
        if (
            destination.x < 0
            or destination.x > 7
            or destination.y < 0
            or destination.y > 0
        ):
            break

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, king.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Movimiento hacia arriba izquierda
    for i in range(1, 2):
        destination = Position(king.position.x - i, king.position.y + i)

        # Si el movimiento está fuera del tablero, no se añade
        if (
            destination.x < 0
            or destination.x > 7
            or destination.y < 0
            or destination.y > 0
        ):
            break

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, king.team):
            possible_moves.append(destination)
            break
        else:
            break

    return possible_moves


def get_castling_moves(king: Piece, board_state: List[Piece]):
    possible_moves: List[Position] = []

    if king.has_moved() and not king.is_checked():
        return possible_moves

    # Sacamos las torres del equipo del rey que no se han movido
    rooks = [
        p for p in board_state if p.is_rook and p.team == king.team and not p.has_moved
    ]

    # Iterar por las torres
    for rook in rooks:
        # Determinar si vamos al lado derecho o izquierdo
        direction = 1 if rook.position.x - king.position.x > 0 else -1
        adjacent_position = king.position.clone()
        adjacent_position.x = adjacent_position.x + direction

        if not (
            rook.possible_moves
            and any(m.same_position(adjacent_position) for m in rook.possible_moves)
        ):
            continue

        # Sabemos que la torre puede moverse al lado adyacente del rey
        concerning_tiles = [m for m in rook.possible_moves if m.y == king.position.y]

        # Verificamos si alguna de las piezas enemigas puede atacar los espacios entre la torre y el rey
        enemy_pieces = [p for p in board_state if p.team != king.team]

        valid = True

        for enemy in enemy_pieces:
            if enemy.possible_moves is None:
                continue

            for move in enemy.possible_moves:
                if any(t.same_position(move) for t in concerning_tiles):
                    valid = False
                    break

            if not valid:
                break

        if not valid:
            continue

        # Ahora queremos agregarla como un movimiento posible
        possible_moves.append(rook.position.clone())

    return possible_moves
