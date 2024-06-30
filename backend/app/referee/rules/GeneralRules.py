
def tile_is_occupied(position, board_state):
    """
    Verifica si una posición está ocupada por alguna pieza en el estado actual del tablero.
    """
    return any(piece.position.same_position(position) for piece in board_state)


def tile_is_occupied_by_opponent(position, board_state, team):
    """
    Verifica si una posición está ocupada por una pieza del equipo contrario.
    """
    return any(
        piece.position.same_position(position) and piece.team != team
        for piece in board_state
    )


def tile_is_empty_or_occupied_by_opponent(position, board_state, team):
    """
    Verifica si una posición está vacía o está ocupada por una pieza del equipo contrario.
    """
    return not tile_is_occupied(position, board_state) or tile_is_occupied_by_opponent(
        position, board_state, team
    )
