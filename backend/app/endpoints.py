from flask import Flask, jsonify, request, render_template
from .db.database import db, setup_db
from .models.Board import Board
from .models.Position import Position
from .models.Types import PieceType, TeamType
from .models.Piece import Piece


def create_app():
    app = Flask(__name__)
    setup_db(app, "postgresql://postgres:1234@localhost:5432/chess_db")

    with app.app_context():
        db.create_all()

    return app


app = create_app()


@app.context_processor
def utility_processor():
    return dict(enumerate=enumerate)

def setup_board():
    # initializing pieces
    pieces = [
        Piece(Position(1, 1), PieceType.ROOK, TeamType.OUR),
        Piece(Position(2, 1), PieceType.KNIGHT, TeamType.OUR),
        Piece(Position(3, 1), PieceType.BISHOP, TeamType.OUR),
        Piece(Position(4, 1), PieceType.QUEEN, TeamType.OUR),
        Piece(Position(5, 1), PieceType.KING, TeamType.OUR),
        Piece(Position(6, 1), PieceType.BISHOP, TeamType.OUR),
        Piece(Position(7, 1), PieceType.KNIGHT, TeamType.OUR),
        Piece(Position(8, 1), PieceType.ROOK, TeamType.OUR),
        Piece(Position(1, 2), PieceType.PAWN, TeamType.OUR),
        Piece(Position(2, 2), PieceType.PAWN, TeamType.OUR),
        Piece(Position(3, 2), PieceType.PAWN, TeamType.OUR),
        Piece(Position(4, 2), PieceType.PAWN, TeamType.OUR),
        Piece(Position(5, 2), PieceType.PAWN, TeamType.OUR),
        Piece(Position(6, 2), PieceType.PAWN, TeamType.OUR),
        Piece(Position(7, 2), PieceType.PAWN, TeamType.OUR),
        Piece(Position(8, 2), PieceType.PAWN, TeamType.OUR),
        Piece(Position(1, 8), PieceType.ROOK, TeamType.OPPONENT),
        Piece(Position(2, 8), PieceType.KNIGHT, TeamType.OPPONENT),
        Piece(Position(3, 8), PieceType.BISHOP, TeamType.OPPONENT),
        Piece(Position(4, 8), PieceType.QUEEN, TeamType.OPPONENT),
        Piece(Position(5, 8), PieceType.KING, TeamType.OPPONENT),
        Piece(Position(6, 8), PieceType.BISHOP, TeamType.OPPONENT),
        Piece(Position(7, 8), PieceType.KNIGHT, TeamType.OPPONENT),
        Piece(Position(8, 8), PieceType.ROOK, TeamType.OPPONENT),
        Piece(Position(1, 7), PieceType.PAWN, TeamType.OPPONENT),
        Piece(Position(2, 7), PieceType.PAWN, TeamType.OPPONENT),
        Piece(Position(3, 7), PieceType.PAWN, TeamType.OPPONENT),
        Piece(Position(4, 7), PieceType.PAWN, TeamType.OPPONENT),
        Piece(Position(5, 7), PieceType.PAWN, TeamType.OPPONENT),
        Piece(Position(6, 7), PieceType.PAWN, TeamType.OPPONENT),
        Piece(Position(7, 7), PieceType.PAWN, TeamType.OPPONENT),
        Piece(Position(8, 7), PieceType.PAWN, TeamType.OPPONENT),
    ]
    return Board(pieces, total_turns=1)


@app.route("/setup_board", methods=["POST"])  # done
def setup_board_route():
    board = setup_board()
    db.session.add(board)
    db.session.commit()
    return jsonify({"message": "Board setup completed"}), 200


@app.route("/move_piece", methods=["POST"])
def move_piece():
    data = request.json
    end_pos = Position(data["end_pos"][0], data["end_pos"][1])
    team = data["team"]

    # Busca la pieza que se desea mover en la base de datos
    position_piece = (
        db.session.query(Position, Piece)
        .join(Piece, Position.id == Piece.position_id)
        .filter(
            Position.x == data["start_pos"][0],
            Position.y == data["start_pos"][1],
            Piece.team == data["team"],
            Piece.board_id == data["board_id"],
        )
        .first()
    )

    if position_piece:
        position, piece = position_piece
        # Verifica si el movimiento es válido para la pieza
        for move in piece.possible_moves:
            goal = Position.from_dict(move).clone()
            if (end_pos.same_position(goal)):
                # Realiza el movimiento en el tablero
                board = (
                    Board.query.first()
                )  # Suponiendo que solo hay un tablero en la base de datos
                if board.play_move(
                    en_passant_move=False,
                    valid_move=True,
                    played_piece=piece,
                    destination=end_pos,
                ):
                    db.session.commit()
                    return jsonify({"message": "Piece moved successfully"}), 200
                else:
                    return jsonify({"error": "Invalid move"}), 400
            else:
                return jsonify({"error": "Invalid move for this piece"}), 400
    else:
        return jsonify({"error": "Piece not found or invalid move"}), 400


# Endpoint para obtener todas las posiciones
@app.route("/positions", methods=["GET"])
def get_positions():
    positions = Position.query.all()
    return jsonify([position.to_dict() for position in positions])


# Endpoint para obtener una posición específica
@app.route("/positions/<int:position_id>", methods=["GET"])
def get_position(position_id):
    position = Position.query.get_or_404(position_id)
    return jsonify(position.to_dict())


# Endpoint para crear una nueva posición
@app.route("/positions", methods=["POST"])
def create_position():
    data = request.get_json()
    new_position = Position(x=data["x"], y=data["y"])
    db.session.add(new_position)
    db.session.commit()
    return jsonify(new_position.to_dict()), 201


# Endpoint para actualizar una posición existente
@app.route("/positions/<int:position_id>", methods=["PUT"])
def update_position(position_id):
    data = request.get_json()
    position = Position.query.get_or_404(position_id)
    position.x = data["x"]
    position.y = data["y"]
    db.session.commit()
    return jsonify(position.to_dict())


# Endpoint para eliminar una posición
@app.route("/positions/<int:position_id>", methods=["DELETE"])
def delete_position(position_id):
    position = Position.query.get_or_404(position_id)
    db.session.delete(position)
    db.session.commit()
    return "", 204


# Endpoint para obtener todas las piezas
@app.route("/pieces", methods=["GET"])
def get_pieces():
    pieces = Piece.query.all()
    return jsonify([piece.to_dict() for piece in pieces])


# Endpoint para obtener una pieza específica
@app.route("/pieces/<int:piece_id>", methods=["GET"])
def get_piece(piece_id):
    piece = Piece.query.get_or_404(piece_id)
    return jsonify(piece.to_dict())


# Endpoint para crear una nueva pieza
@app.route("/pieces", methods=["POST"])
def create_piece():
    data = request.get_json()
    position = Position.query.get_or_404(data["position_id"])
    new_piece = Piece(
        position=position,
        type=data["type"],
        team=data["team"],
        has_moved=data.get("has_moved", False),
        is_checked=data.get("is_checked", False),
    )
    db.session.add(new_piece)
    db.session.commit()
    return jsonify(new_piece.to_dict()), 201


# Endpoint para actualizar una pieza existente
@app.route("/pieces/<int:piece_id>", methods=["PUT"])
def update_piece(piece_id):
    data = request.get_json()
    piece = Piece.query.get_or_404(piece_id)
    piece.position = Position.query.get_or_404(data["position_id"])
    piece.type = data["type"]
    piece.team = data["team"]
    piece.has_moved = data.get("has_moved", piece.has_moved)
    piece.is_checked = data.get("is_checked", piece.is_checked)
    db.session.commit()
    return jsonify(piece.to_dict())


# Endpoint para eliminar una pieza
@app.route("/pieces/<int:piece_id>", methods=["DELETE"])
def delete_piece(piece_id):
    piece = Piece.query.get_or_404(piece_id)
    db.session.delete(piece)
    db.session.commit()
    return "", 204


# Endpoint para obtener el estado del tablero
@app.route("/board", methods=["GET"])
def get_board():
    board = Board.query.first()  # Asumimos que solo hay un tablero
    return jsonify(board.to_dict())


# Endpoint para calcular todos los movimientos posibles
@app.route("/board/calculate_moves", methods=["POST"])
def calculate_all_moves():
    board = Board.query.first()  # Asumimos que solo hay un tablero
    board.calculate_all_moves()
    db.session.commit()
    return jsonify(board.to_dict())


# Endpoint para jugar un movimiento
@app.route("/board/play_move", methods=["POST"])
def play_move():
    data = request.get_json()
    board = Board.query.first()  # Asumimos que solo hay un tablero
    en_passant_move = data["en_passant_move"]
    valid_move = data["valid_move"]
    played_piece = Piece.query.get_or_404(data["played_piece_id"])
    destination = Position.query.get_or_404(data["destination_id"])
    result = board.play_move(en_passant_move, valid_move, played_piece, destination)
    db.session.commit()
    return jsonify({"result": result})

@app.route("/show_board/<int:board_id>", methods = ["GET"])
def show_board(board_id):
    # tablero a retornar
    board_arr = []
    for i in range(8):
        temp = []
        for j in range(8):
            temp.append(" ")
        board_arr.append(temp)

    # obtener las piezas del tablero y sus posiciones

    position_piece = (
        db.session.query(Position, Piece)
        .join(Piece, Position.id == Piece.position_id)
        .filter(
            Piece.board_id == board_id
        )
    )

    for pos, pie in position_piece:
        i = pos.y - 1
        j = pos.x - 1

        board_arr[i][j] = pie.to_char()

    in_del, out_del = " ", '\n'

    board = out_del.join([in_del.join([ele for ele in sub]) for sub in board_arr])

    return render_template("board.html", board=board_arr)


    


if __name__ == "__main__":
    app.run(debug=True)
