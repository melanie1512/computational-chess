'use client';
import "./Referee.css";
import { useEffect, useRef, useState } from "react";
import { initialBoard } from "../../Constants";
import { Piece, Position } from "../../models";
import { Board } from "../../models/Board";
import axios from 'axios';
import { PieceType, TeamType } from "../../Types";
import Chessboard from "../Chessboard/Chessboard";

export default function Referee() {
    
    const [board, setBoard] = useState<Board>(new Board([], 1));
    let board_id

    useEffect(() => {
        axios.get(`http://127.0.0.1:5000/`)
            .then(response => {
                
            })
            .catch(error => console.error('Failed to fetch board:', error));
    }, []);

    const set_vars = (response: any) => {
        let piece_ = response.data["board"]
        let totalTurns = response.data["total_turns"]
        console.log(piece_, "piece_", response.data)
        let piece = []
        for (let i = 0; i < piece_.length; i++) {
            let position = new Position(piece_[i][0][0], piece_[i][0][1])
            let type = piece_[i][1]
            let team = piece_[i][2]
            let hasMoved = false
            let possibleMoves = []
            let id = piece_[i][4]
            if (piece_[i][3].length > 0  ){
                for (let j = 0; j < piece_[i][3].length; j++) {
                    possibleMoves.push(new Position(piece_[i][3][j]['x'], piece_[i][3][j]['y']))
                }
            }
            piece.push(new Piece(id, position, type, team, hasMoved, possibleMoves))
        }
        console.log(piece)
        const newBoard = new Board(piece, totalTurns);
        setBoard(newBoard);
    }

    useEffect(() => {
        const fetchBoard = () => {
            axios.get(`http://127.0.0.1:5000/show_boards/1`)
                .then(response => {
                    set_vars(response)
                })
                .catch(error => console.error('Failed to fetch board:', error));
        }
    
        fetchBoard();
    }, []);

    const [promotionPawn, setPromotionPawn] = useState<Piece>();
    const modalRef = useRef<HTMLDivElement>(null);
    const checkmateModalRef = useRef<HTMLDivElement>(null);
    const stalemateModalRef = useRef<HTMLDivElement>(null);
    let playedMoveIsValid = false;
    //llamar api backend para jugar
    function playMove(playedPiece: Piece, destination: Position): boolean {
        axios.post(`http://127.0.0.1:5000/play_move/1`, {'id': playedPiece.id, 'x': destination.x, 'y': destination.y})
            .then(response => {
                set_vars(response)
                playedMoveIsValid = response.data["result"]
            })
            .catch(error => console.error('Failed to fetch board:', error));

        // This is for promoting a pawn
        let promotionRow = (playedPiece.team === TeamType.OUR) ? 7 : 0;
        //implemnte inside play_move
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

    function promotePawn(pieceType: PieceType) {
        if (promotionPawn === undefined) {
            return;
        }
        axios.post(`http://127.0.0.1:5000/promote_pawn/1`, {'id': promotionPawn.id, 'piece_type': pieceType})
        .then(response => {
            set_vars(response)
        })
        .catch(error => console.error('Failed to fetch board:', error));
        //endpoint to promote pawn

        modalRef.current?.classList.add("hidden");
    }

    function promotionTeamType() {
        return (promotionPawn?.team === TeamType.OUR) ? "w" : "b";
    }
    //request to restart game
    //endpont to restart game
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