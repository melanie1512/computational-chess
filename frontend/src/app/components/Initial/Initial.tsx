'use client';
import React from 'react';
import { useRouter } from 'next/navigation'
import { useEffect, useRef, useState } from "react";
import axios from 'axios';

export default function Initial() {
  const router = useRouter();
  const [boardId, setBoardID] = useState<number>(0);

  useEffect(() => {
    // This will trigger on `boardId` change and navigate to the new path
    const routeChange = () => {
      console.log(boardId, "Navigating to the game...");
      let path = `/Game/${boardId}`;
      router.push(path);
    };

    // Check if the default boardId '1' has changed before navigating
    if (boardId !== 0) {
      routeChange();
    }
  }, [boardId, router]);

  const setVars = (response: any) => {
    let id = response.data["board_id"];
    setBoardID(parseInt(id)); // Update the boardId state
  };

  const createGame = () => {
    axios.get('http://127.0.0.1:5000/')
      .then(response => {
        console.log(response.data["board_id"]);
        if (response.data["board_id"] !== undefined) {
          setVars(response);
        }
      })
      .catch(error => console.error('Failed to fetch board:', error));
  };

  
    return (
      <div className="flex items-center justify-center h-screen" style={{ backgroundColor: '#769656' }}>
        <div className="text-center p-10 rounded-lg" style={{ backgroundColor: '#eeeeee' }}>
          <h1 className="mb-4 text-3xl font-bold" style={{ color: '#333333' }}>Welcome to the Chess Game</h1>
          <button 
            onClick={createGame} 
            className="px-6 py-2 text-lg font-semibold text-white rounded shadow-lg" 
            style={{ backgroundColor: '#333333', borderColor: '#F0D9B5' }}>
            Start Game
          </button>
        </div>
      </div>
    );
}