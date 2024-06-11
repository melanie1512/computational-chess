# rules.py


def is_position_empty(position, board_state):
    for piece in board_state:
        if piece.position.same_position(position):
            return False
    return True


def is_opponent_piece(position, team, board_state):
    for piece in board_state:
        if piece.position.same_position(position) and piece.team != team:
            return True
    return False


def get_possible_pawn_moves(pawn, board_state):
    from app.models import Position, TeamType

    moves = []

    if pawn.team == TeamType.OUR:
        special_row = 1
    else:
        special_row = 6

    if pawn.team == TeamType.OUR:
        pawn_direction = 1
    else:
        pawn_direction = -1

    direction = 1 if pawn.team == TeamType.OUR else -1
    start_row = 1 if pawn.team == TeamType.OUR else 6

    # Movimiento hacia adelante
    forward_position = Position(pawn.position.x, pawn.position.y + direction)
    if is_position_empty(forward_position, board_state):
        moves.append(forward_position)
        # Movimiento doble si es el primer movimiento
        if pawn.position.y == start_row:
            double_forward_position = Position(
                pawn.position.x, pawn.position.y + 2 * direction
            )
            if is_position_empty(double_forward_position, board_state):
                moves.append(double_forward_position)

    # Captura hacia la izquierda
    if pawn.position.x - 1 >= 1 and pawn.position.y + direction <= 8:
        capture_left_position = Position(
            pawn.position.x - 1, pawn.position.y + direction
        )
        if is_opponent_piece(capture_left_position, pawn.team, board_state):
            moves.append(capture_left_position)

    # Captura hacia la derecha
    if pawn.position.x + 1 <= 8 and pawn.position.y + direction <= 8:
        capture_right_position = Position(
            pawn.position.x + 1, pawn.position.y + direction
        )
        if is_opponent_piece(capture_right_position, pawn.team, board_state):
            moves.append(capture_right_position)

    return moves


def get_possible_knight_moves(piece, board_state):
    # Implementar la lógica de los movimientos del caballo
    pass


def get_possible_bishop_moves(piece, board_state):
    # Implementar la lógica de los movimientos del alfil
    pass


def get_possible_rook_moves(piece, board_state):
    # Implementar la lógica de los movimientos de la torre
    pass


def get_possible_queen_moves(piece, board_state):
    # Implementar la lógica de los movimientos de la reina
    pass


def get_possible_king_moves(piece, board_state):
    # Implementar la lógica de los movimientos del rey
    pass


def get_castling_moves(king, board_state):
    # Implementar la lógica del enroque
    pass
