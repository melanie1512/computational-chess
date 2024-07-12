'use client';
import "./Referee.css";
import { useEffect, useRef, useState } from "react";
import axios from 'axios';
import { Piece, Position } from "../../models";
import { Board } from "../../models/Board";
import Chessboard from "../Chessboard/Chessboard";
import { PieceType, TeamType } from "../../Types";

interface Props {
    id: number;
  }

export default function Referee({id}: Props) {
    const [board, setBoard] = useState<Board>(new Board([], 1));
    const [checkmate, setCheckmate] = useState<boolean>(false);
    const [stalemate, setStalemate] = useState<boolean>(false);
    const [kingChecked, setKingChecked] = useState<boolean>(false);

    const boardID = id;
    const modalRef = useRef<HTMLDivElement>(null);
    const checkmateModalRef = useRef<HTMLDivElement>(null);
    const stalemateModalRef = useRef<HTMLDivElement>(null);
    const kingCheckedModalRef = useRef<HTMLDivElement>(null);
    console.log(TeamType.OUR, TeamType.OPPONENT, TeamType.DRAW)

    const set_vars = (response: any) => {
        let piece_ = response.data["board"];
        let totalTurns = response.data["total_turns"];
        let winningTeam = response.data["winning_team"];
        let piece = [];

        for (let i = 0; i < piece_.length; i++) {
            let position = new Position(piece_[i][0][0], piece_[i][0][1]);
            let type = piece_[i][1];
            let team = piece_[i][2];
            let hasMoved = false;
            let possibleMoves = [];
            console.log(piece_)
            let id = piece_[i][4];
            if (piece_[i][3].length > 0) {
                for (let j = 0; j < piece_[i][3].length; j++) {
                    possibleMoves.push(new Position(piece_[i][3][j]['x'], piece_[i][3][j]['y']));
                }
            }
            piece.push(new Piece(id, position, type, team, hasMoved, possibleMoves));
        }
        if (winningTeam === String(TeamType.OUR)) {
            winningTeam = TeamType.OUR;
        }
        if (winningTeam === String(TeamType.OPPONENT)) {
            winningTeam = TeamType.OPPONENT;
        }
        if (winningTeam === String(TeamType.DRAW)) {
            winningTeam = TeamType.DRAW;
        }
        const newBoard = new Board(piece, totalTurns, winningTeam);
        setBoard(newBoard);

        if (winningTeam === TeamType.OUR || winningTeam === TeamType.OPPONENT) {
            checkmateModalRef.current?.classList.remove("hidden");
        } else {
            checkmateModalRef.current?.classList.add("hidden");
        }

        if (winningTeam === TeamType.DRAW) {
            stalemateModalRef.current?.classList.remove("hidden");
        } else {
            stalemateModalRef.current?.classList.add("hidden");
        }

        if (response.data.king_checked) {
            kingCheckedModalRef.current?.classList.remove("hidden");
        } else {
            kingCheckedModalRef.current?.classList.add("hidden");
        }
    }

    useEffect(() => {
        const fetchBoard = () => {
            axios.get(`http://127.0.0.1:5000/show_boards/${boardID}`)
                .then(response => {
                    set_vars(response);
                })
                .catch(error => console.error('Failed to fetch board:', error));
        }

        fetchBoard();
    }, []);

    const [promotionPawn, setPromotionPawn] = useState<Piece>();
    let playedMoveIsValid = false;

    async function playMove(playedPiece: Piece, destination: Position): Promise<boolean> {
        try {
            const response = await axios.post(`http://127.0.0.1:5000/play_move/${boardID}`, {'id': playedPiece.id, 'x': destination.x, 'y': destination.y});
            set_vars(response);
            playedMoveIsValid = response.data["result"];
            if (response.data["total_turns"] % 2 === 0 && playedMoveIsValid) {
                const response_ = await axios.post(`http://127.0.0.1:5000/ai_move/${boardID}`);
                set_vars(response_);
            }
        } catch (error) {
            console.error('Failed to fetch board:', error);
            playedMoveIsValid = false;
        }

        let promotionRow = (playedPiece.team === TeamType.OUR) ? 7 : 0;
        if (destination.y === promotionRow && playedPiece.isPawn) {
            modalRef.current?.classList.remove("hidden");
            setPromotionPawn(() => {
                const clonedPlayedPiece = playedPiece.clone();
                clonedPlayedPiece.position = destination.clone();
                return clonedPlayedPiece;
            });
        }

        return playedMoveIsValid;
    }

    function promotePawn(pieceType: PieceType) {
        if (!promotionPawn) {
            return;
        }
        axios.post(`http://127.0.0.1:5000/promote_pawn/${boardID}`, {'id': promotionPawn.id, 'piece_type': pieceType})
            .then(response => {
                set_vars(response);
            })
            .catch(error => console.error('Failed to fetch board:', error));

        modalRef.current?.classList.add("hidden");
    }

    function promotionTeamType() {
        return (promotionPawn?.team === TeamType.OUR) ? "w" : "b";
    }

    function restartGame() {
        checkmateModalRef.current?.classList.add("hidden");
        stalemateModalRef.current?.classList.add("hidden");
        axios.post(`http://127.0.0.1:5000/reset_board/${boardID}`)
            .then(response => {
                set_vars(response);
            })
            .catch(error => console.error('Failed to fetch board:', error));
    }

    // Esta función envuelve la llamada asíncrona en una función síncrona
    const handlePlayMove = (playedPiece: Piece, destination: Position) => {
        playMove(playedPiece, destination).then(result => {
            return result;
        });
        return playedMoveIsValid;
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
                    <Chessboard playMove={handlePlayMove} pieces={board.pieces} />
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
            <div className="div"> <button onClick={restartGame}>Restart</button></div>
        </>
    );
}
