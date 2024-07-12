from flask import Flask, jsonify, request, render_template
from .db.database import db, setup_db
from .models.Board import Board
from .models.Position import Position
from .models.Types import PieceType, TeamType
from .models.Piece import Piece
from .minimax.functions import minimax, play_move_wrapper
import os
from dotenv import load_dotenv


import logging
# Set up logging	
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

def create_app():
    app = Flask(__name__)
    path = os.getenv("SQLALCHEMY_DATABASE_URI")
    setup_db(app, path)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


@app.context_processor
def utility_processor():
    return dict(enumerate=enumerate)


def setup_board():
    # initializing pieces
    positions = [
        Position(x=1, y=1), Position(x=2, y=1), Position(x=3, y=1), Position(x=4, y=1),
        Position(x=5, y=1), Position(x=6, y=1), Position(x=7, y=1), Position(x=8, y=1),
        Position(x=1, y=2), Position(x=2, y=2), Position(x=3, y=2), Position(x=4, y=2),
        Position(x=5, y=2), Position(x=6, y=2), Position(x=7, y=2), Position(x=8, y=2),
        Position(x=1, y=8), Position(x=2, y=8), Position(x=3, y=8), Position(x=4, y=8),
        Position(x=5, y=8), Position(x=6, y=8), Position(x=7, y=8), Position(x=8, y=8),
        Position(x=1, y=7), Position(x=2, y=7), Position(x=3, y=7), Position(x=4, y=7),
        Position(x=5, y=7), Position(x=6, y=7), Position(x=7, y=7), Position(x=8, y=7),
    ]
    db.session.add_all(positions)
    db.session.commit()

    pieces = [
        Piece(position_id=positions[0].id, type=PieceType.ROOK, team=TeamType.OUR),
        Piece(position_id=positions[1].id, type=PieceType.KNIGHT, team=TeamType.OUR),
        Piece(position_id=positions[2].id, type=PieceType.BISHOP, team=TeamType.OUR),
        Piece(position_id=positions[3].id, type=PieceType.QUEEN, team=TeamType.OUR),
        Piece(position_id=positions[4].id, type=PieceType.KING, team=TeamType.OUR),
        Piece(position_id=positions[5].id, type=PieceType.BISHOP, team=TeamType.OUR),
        Piece(position_id=positions[6].id, type=PieceType.KNIGHT, team=TeamType.OUR),
        Piece(position_id=positions[7].id, type=PieceType.ROOK, team=TeamType.OUR),
        Piece(position_id=positions[8].id, type=PieceType.PAWN, team=TeamType.OUR),
        Piece(position_id=positions[9].id, type=PieceType.PAWN, team=TeamType.OUR),
        Piece(position_id=positions[10].id, type=PieceType.PAWN, team=TeamType.OUR),
        Piece(position_id=positions[11].id, type=PieceType.PAWN, team=TeamType.OUR),
        Piece(position_id=positions[12].id, type=PieceType.PAWN, team=TeamType.OUR),
        Piece(position_id=positions[13].id, type=PieceType.PAWN, team=TeamType.OUR),
        Piece(position_id=positions[14].id, type=PieceType.PAWN, team=TeamType.OUR),
        Piece(position_id=positions[15].id, type=PieceType.PAWN, team=TeamType.OUR),
        Piece(position_id=positions[16].id, type=PieceType.ROOK, team=TeamType.OPPONENT),
        Piece(position_id=positions[17].id, type=PieceType.KNIGHT, team=TeamType.OPPONENT),
        Piece(position_id=positions[18].id, type=PieceType.BISHOP, team=TeamType.OPPONENT),
        Piece(position_id=positions[19].id, type=PieceType.QUEEN, team=TeamType.OPPONENT),
        Piece(position_id=positions[20].id, type=PieceType.KING, team=TeamType.OPPONENT),
        Piece(position_id=positions[21].id, type=PieceType.BISHOP, team=TeamType.OPPONENT),
        Piece(position_id=positions[22].id, type=PieceType.KNIGHT, team=TeamType.OPPONENT),
        Piece(position_id=positions[23].id, type=PieceType.ROOK, team=TeamType.OPPONENT),
        Piece(position_id=positions[24].id, type=PieceType.PAWN, team=TeamType.OPPONENT),
        Piece(position_id=positions[25].id, type=PieceType.PAWN, team=TeamType.OPPONENT),
        Piece(position_id=positions[26].id, type=PieceType.PAWN, team=TeamType.OPPONENT),
        Piece(position_id=positions[27].id, type=PieceType.PAWN, team=TeamType.OPPONENT),
        Piece(position_id=positions[28].id, type=PieceType.PAWN, team=TeamType.OPPONENT),
        Piece(position_id=positions[29].id, type=PieceType.PAWN, team=TeamType.OPPONENT),
        Piece(position_id=positions[30].id, type=PieceType.PAWN, team=TeamType.OPPONENT),
        Piece(position_id=positions[31].id, type=PieceType.PAWN, team=TeamType.OPPONENT),
    ]
    return Board(total_turns=1, pieces=pieces)



@app.route("/")
def index():
    # Verificar si ya existe un tablero
    board = Board.query.first()
    if not board:
        # Si no existe, crear un nuevo tablero
        board = setup_board()
        board.id = 1
        
        db.session.add(board)
        db.session.commit()
    return render_template("index.html", board_id=board.id)

@app.route("/setup_board", methods=["POST"])
def setup_board_route():
    board = setup_board()
    board.id = 1
    db.session.add(board)
    db.session.commit()
    return jsonify({"message": "Board setup completed"}), 200

@app.route("/reset_board/<int:board_id>", methods=["POST"])
def reset_board(board_id):
    board = Board.query.get_or_404(board_id)
    db.session.delete(board)
    db.session.commit()
    board = setup_board()
    board.id = 1
    db.session.add(board)
    db.session.commit()
    return jsonify({"message": "Board reset completed"}), 200

@app.route("/show_board/<int:board_id>", methods=["GET"])
def show_board(board_id):
    # Tablero a retornar
    board_arr = [[" " for _ in range(8)] for _ in range(8)]

    # Obtener las piezas del tablero y sus posiciones
    position_piece = (
        db.session.query(Position, Piece)
        .join(Piece, Position.id == Piece.position_id)
        .filter(Piece.board_id == board_id)
    )

    for pos, pie in position_piece:
        i = pos.y - 1
        j = pos.x - 1
        board_arr[i][j] = pie.to_char()
    
    return jsonify({"board": board_arr})


@app.route("/delete_board/<int:board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = Board.query.get_or_404(board_id)
    db.session.delete(board)
    db.session.commit()
    return jsonify({"message": "Board deleted successfully"}), 200


@app.route("/move_piece", methods=["POST"])
def move_piece():
    data = request.json
    end_pos = Position(data["end_pos"][0], data["end_pos"][1])
    team = data["team"]
    board_id = data["board_id"]

    # Busca la pieza que se desea mover en la base de datos
    position_piece = (
        db.session.query(Position, Piece)
        .join(Piece, Position.id == Piece.position_id)
        .filter(
            Position.x == data["start_pos"][0],
            Position.y == data["start_pos"][1],
            Piece.team == team,
            Piece.board_id == board_id,
        )
        .first()
    )

    if not position_piece:
        return jsonify({"error": "Piece not found or invalid move"}), 400
    
    position, piece = position_piece

    # Verifica si el movimiento es válido para la pieza
    for move in piece.possible_moves:
        goal = Position.from_dict(move).clone()
        if end_pos.same_position(goal):
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
    return jsonify({"error": "Invalid move for this piece"}), 400

# Endpoint para calcular todos los movimientos posibles
@app.route("/board/calculate_moves", methods=["POST"])
def calculate_all_moves():
    board = Board.query.first()  # Asumimos que solo hay un tablero
    board.calculate_all_moves()
    db.session.commit()
    return jsonify(board.to_dict())

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
    boards = Board.query.all()  # Asumimos que solo hay un tablero
    return jsonify([board.to_dict() for board in boards])

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

@app.route("/ai_move", methods=["POST"])
def ai_move():
    board = Board.query.first()  # Asumiendo que solo hay un tablero

    with db.session() as session:
        _, best_move = minimax(board, depth=2, alpha=float('-inf'), beta=float('inf'), maximizing_player=False, session=session)

    if best_move:
        print(best_move["played_piece"].to_dict())
        print(best_move["destination"].to_dict())

        en_passant_move = False
        valid_move = True
        played_piece =  Piece.query.get_or_404(best_move["played_piece"].id)

        db.session.add(played_piece)
        destination = best_move["destination"]
        db.session.add(destination)
        result = board.play_move(en_passant_move, valid_move, played_piece, destination)

        db.session.commit()
        return jsonify({"message": "AI move completed"}), 200
    else:
        return jsonify({"error": "No valid moves found"}), 400


if __name__ == "__main__":
    app.run(debug=True)
