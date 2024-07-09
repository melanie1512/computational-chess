import { TeamType, PieceType } from "../Types";
import { Position } from "./Position";

export class Piece {
    id: number;
    image: string;
    position: Position;
    type: PieceType;
    team: TeamType;
    possibleMoves?: Position[];
    hasMoved: boolean;
    isChecked?: boolean;
    constructor(id: number, position: Position, type: PieceType,
        team: TeamType, hasMoved: boolean,
        possibleMoves: Position[] = []) {
        this.id = id;
        this.image = `assets/images/${type}_${team === 1? 'w': 'b'}.png`;
        this.position = position;
        this.type = type;
        this.team = team;
        this.possibleMoves = possibleMoves;
        this.hasMoved = hasMoved;
        this.isChecked = false;
    }

    get isPawn() : boolean {
        return this.type === PieceType.PAWN
    }

    get isRook() : boolean {
        return this.type === PieceType.ROOK
    }

    get isKnight() : boolean {
        return this.type === PieceType.KNIGHT
    }

    get isBishop() : boolean {
        return this.type === PieceType.BISHOP
    }

    get isKing() : boolean {
        return this.type === PieceType.KING
    }

    get isQueen() : boolean {
        return this.type === PieceType.QUEEN
    }

    samePiecePosition(otherPiece: Piece) : boolean {
        return this.position.samePosition(otherPiece.position);
    }

    samePosition(otherPosition: Position) : boolean {
        return this.position.samePosition(otherPosition);
    }

    clone(): Piece {
        return new Piece(this.id, this.position.clone(),
             this.type, this.team, this.hasMoved,
             this.possibleMoves?.map(m => m.clone()));
    }
}