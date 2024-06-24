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
        multiplier_x = -1 if desired_position.x < initial_position.x else 1 if desired_position.x > initial_position.x else 0
        multiplier_y = -1 if desired_position.y < initial_position.y else 1 if desired_position.y > initial_position.y else 0
        
        passed_position = Position(initial_position + (i * multiplier_x), initial_position.y + (i * multiplier_y))

        if (passed_position.same_position(desired_position)):
            if (tile_is_empty_or_occupied_by_opponent(passed_position, board_state, team)):
                return True
        else:
            if (tile_is_occupied(passed_position, board_state)):
                break
    return False

def get_possible_king_moves(king: Piece, board_state: List[Piece]):
    possible_moves: List[Position] = []

    # Movimiento hacia arriba
    for i in range(1,2):
        destination = Position(king.position.x, king.position.y + i)

        # Si el movimiento está fuera del tablero, no se añade
        if (destination.x < 0 or destination.x > 7 or destination.y < 0 or destination.y > 0):
            break

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, king.team):
            possible_moves.append(destination)
            break
        else:
            break

    # Movimiento hacia abajo
    for i in range(1,2):
        destination = Position(king.position.x, king.position.y - i)

        # Si el movimiento está fuera del tablero, no se añade
        if (destination.x < 0 or destination.x > 7 or destination.y < 0 or destination.y > 0):
            break

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, king.team):
            possible_moves.append(destination)
            break
        else:
            break
    
    # Movimiento hacia la izquierda
    for i in range(1,2):
        destination = Position(king.position.x - i, king.position.y)

        # Si el movimiento está fuera del tablero, no se añade
        if (destination.x < 0 or destination.x > 7 or destination.y < 0 or destination.y > 0):
            break

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, king.team):
            possible_moves.append(destination)
            break
        else:
            break
    
    # Movimiento hacia la derecha
    for i in range(1,2):
        destination = Position(king.position.x + i, king.position.y)

        # Si el movimiento está fuera del tablero, no se añade
        if (destination.x < 0 or destination.x > 7 or destination.y < 0 or destination.y > 0):
            break

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, king.team):
            possible_moves.append(destination)
            break
        else:
            break
    
    # Movimiento hacia arriba derecha
    for i in range(1,2):
        destination = Position(king.position.x + i, king.position.y + i)

        # Si el movimiento está fuera del tablero, no se añade
        if (destination.x < 0 or destination.x > 7 or destination.y < 0 or destination.y > 0):
            break

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, king.team):
            possible_moves.append(destination)
            break
        else:
            break
    
    # Movimiento hacia abajo derecha
    for i in range(1,2):
        destination = Position(king.position.x + i, king.position.y - i)

        # Si el movimiento está fuera del tablero, no se añade
        if (destination.x < 0 or destination.x > 7 or destination.y < 0 or destination.y > 0):
            break

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, king.team):
            possible_moves.append(destination)
            break
        else:
            break
    
    # Movimiento hacia abajo izquierda
    for i in range(1,2):
        destination = Position(king.position.x - i, king.position.y - i)

        # Si el movimiento está fuera del tablero, no se añade
        if (destination.x < 0 or destination.x > 7 or destination.y < 0 or destination.y > 0):
            break

        if not tile_is_occupied(destination, board_state):
            possible_moves.append(destination)
        elif tile_is_occupied_by_opponent(destination, board_state, king.team):
            possible_moves.append(destination)
            break
        else:
            break
    
    # Movimiento hacia arriba izquierda
    for i in range(1,2):
        destination = Position(king.position.x - i, king.position.y + i)

        # Si el movimiento está fuera del tablero, no se añade
        if (destination.x < 0 or destination.x > 7 or destination.y < 0 or destination.y > 0):
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

    if (king.has_moved() and not king.is_checked()):
        return possible_moves
    
    # Sacamos las torres del equipo del rey que no se han movido
    rooks = [p for p in board_state if p.is_rook and p.team == king.team and not p.has_moved]

    # Iterar por las torres
    for rook in rooks:
        # Determinar si vamos al lado derecho o izquierdo
        direction = 1 if rook.position.x - king.position.x > 0 else -1
        
