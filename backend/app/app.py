from flask import Flask, jsonify, request
from .database import init_db, db
from .models import Piece, Position, Board


def create_app():
    app = Flask(__name__)
    init_db(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


# Endpoint para obtener todas las posiciones
@app.route('/positions', methods=['GET'])
def get_positions():
    positions = Position.query.all()
    return jsonify([position.to_dict() for position in positions])

# Endpoint para obtener una posición específica
@app.route('/positions/<int:position_id>', methods=['GET'])
def get_position(position_id):
    position = Position.query.get_or_404(position_id)
    return jsonify(position.to_dict())

# Endpoint para crear una nueva posición
@app.route('/positions', methods=['POST'])
def create_position():
    data = request.get_json()
    new_position = Position(x=data['x'], y=data['y'])
    db.session.add(new_position)
    db.session.commit()
    return jsonify(new_position.to_dict()), 201

# Endpoint para actualizar una posición existente
@app.route('/positions/<int:position_id>', methods=['PUT'])
def update_position(position_id):
    data = request.get_json()
    position = Position.query.get_or_404(position_id)
    position.x = data['x']
    position.y = data['y']
    db.session.commit()
    return jsonify(position.to_dict())

# Endpoint para eliminar una posición
@app.route('/positions/<int:position_id>', methods=['DELETE'])
def delete_position(position_id):
    position = Position.query.get_or_404(position_id)
    db.session.delete(position)
    db.session.commit()
    return '', 204

# Endpoint para obtener todas las piezas
@app.route('/pieces', methods=['GET'])
def get_pieces():
    pieces = Piece.query.all()
    return jsonify([piece.to_dict() for piece in pieces])

# Endpoint para obtener una pieza específica
@app.route('/pieces/<int:piece_id>', methods=['GET'])
def get_piece(piece_id):
    piece = Piece.query.get_or_404(piece_id)
    return jsonify(piece.to_dict())

# Endpoint para crear una nueva pieza
@app.route('/pieces', methods=['POST'])
def create_piece():
    data = request.get_json()
    position = Position.query.get_or_404(data['position_id'])
    new_piece = Piece(
        position=position,
        type=data['type'],
        team=data['team'],
        has_moved=data.get('has_moved', False),
        is_checked=data.get('is_checked', False)
    )
    db.session.add(new_piece)
    db.session.commit()
    return jsonify(new_piece.to_dict()), 201

# Endpoint para actualizar una pieza existente
@app.route('/pieces/<int:piece_id>', methods=['PUT'])
def update_piece(piece_id):
    data = request.get_json()
    piece = Piece.query.get_or_404(piece_id)
    piece.position = Position.query.get_or_404(data['position_id'])
    piece.type = data['type']
    piece.team = data['team']
    piece.has_moved = data.get('has_moved', piece.has_moved)
    piece.is_checked = data.get('is_checked', piece.is_checked)
    db.session.commit()
    return jsonify(piece.to_dict())

# Endpoint para eliminar una pieza
@app.route('/pieces/<int:piece_id>', methods=['DELETE'])
def delete_piece(piece_id):
    piece = Piece.query.get_or_404(piece_id)
    db.session.delete(piece)
    db.session.commit()
    return '', 204

# Endpoint para obtener el estado del tablero
@app.route('/board', methods=['GET'])
def get_board():
    board = Board.query.first()  # Asumimos que solo hay un tablero
    return jsonify(board.to_dict())

# Endpoint para calcular todos los movimientos posibles
@app.route('/board/calculate_moves', methods=['POST'])
def calculate_all_moves():
    board = Board.query.first()  # Asumimos que solo hay un tablero
    board.calculate_all_moves()
    db.session.commit()
    return jsonify(board.to_dict())

# Endpoint para jugar un movimiento
@app.route('/board/play_move', methods=['POST'])
def play_move():
    data = request.get_json()
    board = Board.query.first()  # Asumimos que solo hay un tablero
    en_passant_move = data['en_passant_move']
    valid_move = data['valid_move']
    played_piece = Piece.query.get_or_404(data['played_piece_id'])
    destination = Position.query.get_or_404(data['destination_id'])
    result = board.play_move(en_passant_move, valid_move, played_piece, destination)
    db.session.commit()
    return jsonify({'result': result})


if __name__ == "__app__":
    app.run(debug=True)
