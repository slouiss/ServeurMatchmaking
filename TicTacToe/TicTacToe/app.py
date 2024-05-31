from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

boardState = [""] * 9
currentPlayer = "X"
game_mode = None

def check_winner(board, player):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combination in winning_combinations:
        if all(board[pos] == player for pos in combination):
            return True
    return False

def play_ai_move():
    global boardState, currentPlayer
    available_positions = [i for i, x in enumerate(boardState) if x == ""]
    if available_positions:
        move_position = random.choice(available_positions)
        boardState[move_position] = currentPlayer
        return move_position
    return None

@app.route('/')
def index():
    return render_template('game_mode.html')

@app.route('/game')
def game():
    global game_mode
    game_mode = request.args.get('mode')
    return render_template('index.html', boardState=boardState)

@socketio.on('join_queue')
def handle_join_queue(data):
    emit('queue_joined', {'message': 'You have joined the queue'})

@socketio.on('play_move')
def handle_play_move(data):
    global boardState, currentPlayer, game_mode
    match_id = data['match_id']
    move_position = data['move_position']

    if boardState[move_position] == "":
        boardState[move_position] = currentPlayer
        emit('move_played', {'move_position': move_position, 'player': currentPlayer}, broadcast=True)

        if check_winner(boardState, currentPlayer):
            emit('match_finished', {'message': f'Player {currentPlayer} wins!', 'winner': currentPlayer},
                 broadcast=True)
            return

        if game_mode == "player_vs_player":
            currentPlayer = "O" if currentPlayer == "X" else "X"
        elif game_mode == "player_vs_ai":
            currentPlayer = "O"
            move_position = play_ai_move()
            emit('move_played', {'move_position': move_position, 'player': currentPlayer}, broadcast=True)
            if check_winner(boardState, currentPlayer):
                emit('match_finished', {'message': f'Player {currentPlayer} wins!', 'winner': currentPlayer},
                     broadcast=True)
            currentPlayer = "X"
        elif game_mode == "ai_vs_ai":
            while True:
                move_position = play_ai_move()
                emit('move_played', {'move_position': move_position, 'player': currentPlayer}, broadcast=True)
                if check_winner(boardState, currentPlayer):
                    emit('match_finished', {'message': f'Player {currentPlayer} wins!', 'winner': currentPlayer},
                         broadcast=True)
                    return
                currentPlayer = "O" if currentPlayer == "X" else "X"
                if not any(pos == "" for pos in boardState):
                    break
    else:
        emit('invalid_move', {'message': 'Invalid move'})

@socketio.on('replay_game')
def handle_replay_game():
    global boardState, currentPlayer
    boardState = [""] * 9
    currentPlayer = "X"
    emit('game_reset', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
