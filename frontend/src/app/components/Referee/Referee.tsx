'use client';
import "./Referee.css";
import { useEffect, useRef, useState } from "react";
import { initialBoard } from "../../Constants";
import { Piece, Position } from "../../models";
import { Board } from "../../models/Board";
import { Pawn } from "../../models/Pawn";
import axios from 'axios';
import { bishopMove, kingMove, knightMove, pawnMove, queenMove, rookMove } from "../../referee/rules";
import { PieceType, TeamType } from "../../Types";
import Chessboard from "../Chessboard/Chessboard";

export default function Referee() {
    
    const [board, setBoard] = useState<Board>(new Board([], 1));
    
    useEffect(() => {
        axios.get(`http://127.0.0.1:5000/show_boards/1`)
            .then(response => {
                let piece_ = response.data["board"]
                let totalTurns = response.data["total_turns"]
                console.log(piece_, "piece_")
                let piece = []
                for (let i = 0; i < piece_.length; i++) {
                    let position = new Position(piece_[i][0][1], piece_[i][0][0])
                    let type = piece_[i][1]
                    let team = piece_[i][2]
                    let hasMoved = false
                    let possibleMoves = []
                    if (piece_[i][3].length > 0  ){
                        for (let j = 0; j < piece_[i][3].length; j++) {
                            possibleMoves.push(new Position(piece_[i][3][j]['x'], piece_[i][3][j]['y']))
                        }
                    }
                    piece.push(new Piece(position, type, team, hasMoved, possibleMoves))
                }
                console.log(piece)
                const newBoard = new Board(piece, totalTurns);
                setBoard(newBoard);
            })
            .catch(error => console.error('Failed to fetch board:', error));
    }, []);

    const [promotionPawn, setPromotionPawn] = useState<Piece>();
    const modalRef = useRef<HTMLDivElement>(null);
    const checkmateModalRef = useRef<HTMLDivElement>(null);
    const stalemateModalRef = useRef<HTMLDivElement>(null);

    function playMove(playedPiece: Piece, destination: Position): boolean {
        // If the playing piece doesn't have any moves return
        if (playedPiece.possibleMoves === undefined) return false;

        // Prevent the inactive team from playing
        if (playedPiece.team === TeamType.OUR
            && board.totalTurns % 2 !== 1) return false;
        if (playedPiece.team === TeamType.OPPONENT
            && board.totalTurns % 2 !== 0) return false;

        let playedMoveIsValid = false;

        const validMove = playedPiece.possibleMoves?.some(m => m.samePosition(destination));

        if (!validMove) return false;

        const enPassantMove = isEnPassantMove(
            playedPiece.position,
            destination,
            playedPiece.type,
            playedPiece.team
        );

        // playMove modifies the board thus we
        // need to call setBoard
        setBoard(() => {
            const clonedBoard = board.clone();
            clonedBoard.totalTurns += 1;
            // Playing the move
            playedMoveIsValid = clonedBoard.playMove(enPassantMove,
                validMove, playedPiece,
                destination);

            if (clonedBoard.winningTeam !== undefined && clonedBoard.winningTeam !== TeamType.DRAW) {
                checkmateModalRef.current?.classList.remove("hidden");
            }
            else if (clonedBoard.winningTeam === TeamType.DRAW) {
                stalemateModalRef.current?.classList.remove("hidden");
            }

            return clonedBoard;
        })

        // This is for promoting a pawn
        let promotionRow = (playedPiece.team === TeamType.OUR) ? 7 : 0;

        if (destination.y === promotionRow && playedPiece.isPawn) {
            modalRef.current?.classList.remove("hidden");
            setPromotionPawn((previousPromotionPawn) => {
                const clonedPlayedPiece = playedPiece.clone();
                clonedPlayedPiece.position = destination.clone();
                return clonedPlayedPiece;
            });
        }

        return playedMoveIsValid;
    }

    function isEnPassantMove(
        initialPosition: Position,
        desiredPosition: Position,
        type: PieceType,
        team: TeamType
    ) {
        const pawnDirection = team === TeamType.OUR ? 1 : -1;

        if (type === PieceType.PAWN) {
            if (
                (desiredPosition.x - initialPosition.x === -1 ||
                    desiredPosition.x - initialPosition.x === 1) &&
                desiredPosition.y - initialPosition.y === pawnDirection
            ) {
                const piece = board.pieces.find(
                    (p) =>
                        p.position.x === desiredPosition.x &&
                        p.position.y === desiredPosition.y - pawnDirection &&
                        p.isPawn &&
                        (p as Pawn).enPassant
                );
                if (piece) {
                    return true;
                }
            }
        }

        return false;
    }

    //TODO
    //Add stalemate!
    // request to valid move
    function isValidMove(initialPosition: Position, desiredPosition: Position, type: PieceType, team: TeamType) {
        let validMove = false;
        switch (type) {
            case PieceType.PAWN:
                validMove = pawnMove(initialPosition, desiredPosition, team, board.pieces);
                break;
            case PieceType.KNIGHT:
                validMove = knightMove(initialPosition, desiredPosition, team, board.pieces);
                break;
            case PieceType.BISHOP:
                validMove = bishopMove(initialPosition, desiredPosition, team, board.pieces);
                break;
            case PieceType.ROOK:
                validMove = rookMove(initialPosition, desiredPosition, team, board.pieces);
                break;
            case PieceType.QUEEN:
                validMove = queenMove(initialPosition, desiredPosition, team, board.pieces);
                break;
            case PieceType.KING:
                validMove = kingMove(initialPosition, desiredPosition, team, board.pieces);
        }

        return validMove;
    }

    function promotePawn(pieceType: PieceType) {
        if (promotionPawn === undefined) {
            return;
        }

        setBoard((previousBoard) => {
            const clonedBoard = board.clone();
            clonedBoard.pieces = clonedBoard.pieces.reduce((results, piece) => {
                if (piece.samePiecePosition(promotionPawn)) {
                    results.push(new Piece(piece.position.clone(), pieceType,
                        piece.team, true));
                } else {
                    results.push(piece);
                }
                return results;
            }, [] as Piece[]);

            clonedBoard.calculateAllMoves();

            return clonedBoard;
        })

        modalRef.current?.classList.add("hidden");
    }

    function promotionTeamType() {
        return (promotionPawn?.team === TeamType.OUR) ? "w" : "b";
    }
    //request to restart game
    function restartGame() {
        checkmateModalRef.current?.classList.add("hidden");
        stalemateModalRef.current?.classList.add("hidden");
        setBoard(initialBoard.clone());
    }

    return (
        <>
            <p style={{ color: "white", fontSize: "24px", textAlign: "center" }}>Total turns: {board.totalTurns}</p>
            <div className="modal hidden" ref={modalRef}>
                <div className="modal-body">
                    <img onClick={() => promotePawn(PieceType.ROOK)} src={`/assets/images/rook_${promotionTeamType()}.png`} />
                    <img onClick={() => promotePawn(PieceType.BISHOP)} src={`/assets/images/bishop_${promotionTeamType()}.png`} />
                    <img onClick={() => promotePawn(PieceType.KNIGHT)} src={`/assets/images/knight_${promotionTeamType()}.png`} />
                    <img onClick={() => promotePawn(PieceType.QUEEN)} src={`/assets/images/queen_${promotionTeamType()}.png`} />
                </div>
            </div>
            <div className="modal hidden" ref={checkmateModalRef}>
                <div className="modal-body">
                    <div className="checkmate-body">
                        <span>{board.winningTeam === TeamType.OUR ? "Congratulations! You won" : "You lose :c"}!</span>
                        <button onClick={restartGame}>Play again</button>
                    </div>
                </div>
            </div>
            <div className="modal hidden" ref={stalemateModalRef}>
                <div className="modal-body">
                    <div className="checkmate-body">
                        <span>Its a Draw!</span>
                        <button onClick={restartGame}>Play again</button>
                    </div>
                </div>
            </div>
            <div className="cont">
                <div className="Playzone">
                    <div className="coordinate-y">
                        <div className="number">8</div>
                        <div className="number">7</div>
                        <div className="number">6</div>
                        <div className="number">5</div>
                        <div className="number">4</div>
                        <div className="number">3</div>
                        <div className="number">2</div>
                        <div className="number">1</div>
                    </div>
                    <Chessboard playMove={playMove}
                        pieces={board.pieces} />
                </div>
                <div className="coordinates-x">
                    <div className="character"></div>
                    <div className="character">a</div>
                    <div className="character">b</div>
                    <div className="character">c</div>
                    <div className="character">d</div>
                    <div className="character">e</div>
                    <div className="character">f</div>
                    <div className="character">g</div>
                    <div className="character">h</div>
                </div>
            </div>
        </>
    )
}