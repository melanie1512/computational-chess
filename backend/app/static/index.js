document.addEventListener('DOMContentLoaded', () => {
    const boardId = 1;
    let selectedPiece = null;

    function fetchPossibleMoves(x, y, team) {
        fetch('/get_possible_moves', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                x: x,
                y: y,
                team: team,
                board_id: boardId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                console.log(data.possible_moves);
                console.log(selectedPiece);
                console.log(x, y, team, boardId)
            } else {
                highlightMoves(data.possible_moves);
            }
        });
    }

    function highlightMoves(moves) {
        clearHighlights();
        moves.forEach(move => {
            const cell = document.querySelector(`[data-x='${move.x}'][data-y='${move.y}']`);
            if (cell) {
                cell.classList.add('highlight');
            }
        });
    }

    function clearHighlights() {
        document.querySelectorAll('.highlight').forEach(cell => {
            cell.classList.remove('highlight');
        });
    }

    function makeMove(startX, startY, endX, endY, team) {
        fetch('/move_piece', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                start_pos: [startX, startY],
                end_pos: [endX, endY],
                team: team,
                board_id: boardId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                console.log(startX, startY, endX, endY, team, boardId)
            } else {
                updateBoard();
            }
        });
    }

    function updateBoard() {
        fetch(`/show_board/${boardId}`)
        .then(response => response.json())
        .then(data => {
            const boardContainer = document.getElementById('board-container');
            const board = data.board;
            let html = '<table>';
            for (let i = 0; i < board.length; i++) {
                html += '<tr>';
                for (let j = 0; j < board[i].length; j++) {
                    const color = (i + j) % 2 === 0 ? 'white' : 'black';
                    html += `<td class="${color}" data-x="${j + 1}" data-y="${i + 1}">`;
                    html += `<span class="coordinate">[${j + 1},${i + 1}]</span>`;
                    html += board[i][j];
                    html += '</td>';
                }
                html += '</tr>';
            }
            html += '</table>';
            boardContainer.innerHTML = html;
            addCellListeners();
        });
    }

    function addCellListeners() {
        document.querySelectorAll('td').forEach(cell => {
            cell.addEventListener('click', () => {
                const x = parseInt(cell.getAttribute('data-x'));
                const y = parseInt(cell.getAttribute('data-y'));
                const team = document.querySelector('input[name="team"]:checked').value;

                if (selectedPiece) {
                    makeMove(selectedPiece.x, selectedPiece.y, x, y, team);
                    selectedPiece = null;
                    clearHighlights();
                } else {
                    selectedPiece = { x, y };
                    fetchPossibleMoves(x, y, team);
                }
            });
        });
    }

    document.getElementById('setup-reset-btn').addEventListener('click', function() {
        fetch('/reset_board/' + boardId, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                updateBoard();
            }
        });
    });

    updateBoard();
});
