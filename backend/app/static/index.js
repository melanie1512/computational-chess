document.addEventListener('DOMContentLoaded', () => {
    const boardId = 1;

    function calculateMovesAndMakeMove() {
        fetch('/board/calculate_moves', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data =>{
            makeMove();
        });
    }

    function aiMove(){
        fetch('/ai_move', {
            method: 'POST'
        })
        .then(response => response.json())
    }

    function makeMove() {
        const startPosX = document.getElementById('start_pos_x').value;
        const startPosY = document.getElementById('start_pos_y').value;
        const endPosX = document.getElementById('end_pos_x').value;
        const endPosY = document.getElementById('end_pos_y').value;
        const team = document.querySelector('input[name="team"]:checked').value;

        fetch('/move_piece', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                start_pos: [parseInt(startPosX), parseInt(startPosY)],
                end_pos: [parseInt(endPosX), parseInt(endPosY)],
                team: team,
                board_id: boardId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                updateBoard();
                aiMove();
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
                    html += `<td class="${color}">`;
                    html += `<span class="coordinate">[${j + 1},${i + 1}]</span>`;
                    html += board[i][j];
                    html += '</td>';
                }
                html += '</tr>';
            }
            html += '</table>';
            boardContainer.innerHTML = html;
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

    document.getElementById('play-move-btn').addEventListener('click', calculateMovesAndMakeMove);

    updateBoard();
});
