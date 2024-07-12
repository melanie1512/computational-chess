import { TeamType } from "../Types";
import { Piece } from "./Piece";

export class Board {
    pieces: Piece[];
    totalTurns: number;
    winningTeam?: TeamType;

    constructor(pieces: Piece[], totalTurns: number, winningTeam?: TeamType) {
        this.pieces = pieces;
        this.totalTurns = totalTurns;
        this.winningTeam = winningTeam
    }

    get currentTeam(): TeamType {
        return this.totalTurns % 2 === 0 ? TeamType.OPPONENT : TeamType.OUR;
    }


    clone(): Board {
        return new Board(this.pieces.map(p => p.clone()),
            this.totalTurns);
    }
}