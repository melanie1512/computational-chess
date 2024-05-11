'use client';
import { useRef, useState } from "react";
import "./Chessboard.css";
import Tile from "../Tile/Tile";
import {
  VERTICAL_AXIS,
  HORIZONTAL_AXIS,
} from "../../Constants";
import { Piece, Position } from "../../models";



interface Props {
  playMove: (piece: Piece, position: Position) => boolean;
  pieces: Piece[];
}

export default function Chessboard({playMove, pieces} : Props) {
  const [activePiece, setActivePiece] = useState<HTMLElement | null>(null);
  const [grabPosition, setGrabPosition] = useState<Position>(new Position(-1, -1));
  const chessboardRef = useRef<HTMLDivElement>(null);

  function grabPiece(e: React.MouseEvent) {
    const element = e.target as HTMLElement;
    const chessboard = chessboardRef.current;
    
    const height = element.clientHeight;
    const width = element.clientWidth;

    const GRID_SIZE = height;

    if (element.classList.contains("chess-piece") && chessboard) {
      const grabX = Math.floor((e.clientX - chessboard.offsetLeft) / GRID_SIZE);  
      const grabY = Math.abs(Math.abs(
        Math.ceil((e.clientY - chessboard.offsetTop - height) / GRID_SIZE)
      ) - 7);
      setGrabPosition(new Position(grabX, grabY));

      const x = e.clientX - GRID_SIZE / 2;
      const y = e.clientY - GRID_SIZE / 2;
      element.style.position = "absolute";
      element.style.left = `${x}px`;
      element.style.top = `${y}px`;
      element.style.height = `${height}px`;
      element.style.width = `${width}px`;
      
      setActivePiece(element);
    }
  }

  function movePiece(e: React.MouseEvent) {
    const chessboard = chessboardRef.current;
    if (activePiece && chessboard) {
      const height = activePiece.clientHeight / 4;
      const minX = chessboard.offsetLeft - height;
      const minY = chessboard.offsetTop - height;
      const maxX = chessboard.offsetLeft + chessboard.clientWidth - height*3;
      const maxY = chessboard.offsetTop + chessboard.clientHeight - height*3;
      const x = e.clientX - height*2;
      const y = e.clientY - height*2;
      activePiece.style.position = "absolute";

      //If x is smaller than minimum amount
      if (x < minX) {
        activePiece.style.left = `${minX}px`;
      }
      //If x is bigger than maximum amount
      else if (x > maxX) {
        activePiece.style.left = `${maxX}px`;
      }
      //If x is in the constraints
      else {
        activePiece.style.left = `${x}px`;
      }

      //If y is smaller than minimum amount
      if (y < minY) {
        activePiece.style.top = `${minY}px`;
      }
      //If y is bigger than maximum amount
      else if (y > maxY) {
        activePiece.style.top = `${maxY}px`;
      }
      //If y is in the constraints
      else {
        activePiece.style.top = `${y}px`;
      }
    }
  }

  function dropPiece(e: React.MouseEvent) {
    
    const element = e.target as HTMLElement;
    const chessboard = chessboardRef.current;    
    const height = element.clientHeight;
    const width = element.clientWidth;
    
    const GRID_SIZE = height;
    if (activePiece && chessboard) {
      const x = Math.floor((e.clientX - chessboard.offsetLeft) / GRID_SIZE);
      const y = Math.abs(Math.abs(
        Math.ceil((e.clientY - chessboard.offsetTop - height) / GRID_SIZE)
      ) - 7);

      const currentPiece = pieces.find((p) =>
        p.samePosition(grabPosition)
      );

      if (currentPiece) {
        let tmp = currentPiece.clone();
        var succes = playMove(currentPiece.clone(), new Position(x, y));
        if(!succes) {
          //RESETS THE PIECE POSITION
          activePiece.style.position = "relative";
          activePiece.style.height = "100%";
          activePiece.style.width = "100%";
          activePiece.style.removeProperty("top");
          activePiece.style.removeProperty("left");
        }
      }
      setActivePiece(null);
    }
  }

  let board = [];

  for (let j = VERTICAL_AXIS.length - 1; j >= 0; j--) {
    for (let i = 0; i < HORIZONTAL_AXIS.length; i++) {
      const number = j + i + 2;
      const piece = pieces.find((p) =>
        p.samePosition(new Position(i, j))
      );
      let image = piece ? piece.image : undefined;

      let currentPiece = activePiece != null ? pieces.find(p => p.samePosition(grabPosition)) : undefined;
      let highlight = currentPiece?.possibleMoves ? 
      currentPiece.possibleMoves.some(p => p.samePosition(new Position(i, j))) : false;

      board.push(<Tile key={`${j},${i}`} image={image} number={number} highlight={highlight} />);
    }
  }

  return (
    <>
      <div
        onMouseMove={(e) => movePiece(e)}
        onMouseDown={(e) => grabPiece(e)}
        onMouseUp={(e) => dropPiece(e)}
        id="chessboard"
        ref={chessboardRef}
      >
        {board}
      </div>
    </>
  );
}