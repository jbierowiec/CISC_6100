'''
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

BACKEND_URL = "http://127.0.0.1:8000/sudoku"

@app.route('/')
def index():
    # Fetch the current puzzle from the backend
    puzzle = requests.get(f"{BACKEND_URL}/get_puzzle/").json()
    return render_template('index.html', puzzle=puzzle["puzzle"])

@app.route('/check_solution', methods=['POST'])
def check_solution():
    solution = request.json.get("solution")
    response = requests.post(f"{BACKEND_URL}/check_solution/", json={"solution": solution})
    return jsonify(response.json())

@app.route('/new_game', methods=['GET'])
def new_game():
    # Fetch a new puzzle from the backend
    puzzle = requests.get(f"{BACKEND_URL}/new_game/").json()
    return jsonify(puzzle)
'''

'''
from flask import Flask, render_template, request, jsonify
import requests
import json, random

app = Flask(__name__)

# This is where we store the current board and history of moves
HISTORY = []  # Stack to track move history
current_board = []  # 2D array to represent the current Sudoku board

BACKEND_URL = "http://127.0.0.1:8000/sudoku"

# Load the games from the JSON file
with open('games.json') as f:
    games_data = json.load(f)["sudoku_games"]

def flatten_board():
    """Flatten the board to a single list to send to the frontend for rendering."""
    return [item for row in current_board for item in row]

@app.route('/')
def index():
    # Fetch the current puzzle from the backend
    puzzle = requests.get(f"{BACKEND_URL}/get_puzzle/").json()
    global current_board
    current_board = puzzle["puzzle"]  # Initialize the current board with the puzzle
    return render_template('index.html', puzzle=puzzle["puzzle"])

@app.route('/undo', methods=['POST'])
def undo_move():
    if len(HISTORY) > 0:
        # Pop the last move from history
        square = HISTORY.pop()
        row, col, previous_value = square
        current_board[row][col] = previous_value  # Revert the board cell to previous value
        return jsonify({'status': 'success', 'board': flatten_board()})
    else:
        return jsonify({'status': 'error', 'message': 'No move to undo'})

@app.route('/track_move', methods=['POST'])
def track_move():
    data = request.json
    row = data['row']
    col = data['col']
    new_value = data['value']
    previous_value = current_board[row][col]

    # Store the move in history
    HISTORY.append((row, col, previous_value))
    # Update the board with the new value
    current_board[row][col] = new_value

    return jsonify({'status': 'success'})

@app.route('/check_solution', methods=['POST'])
def check_solution():
    solution = request.json.get("solution")
    response = requests.post(f"{BACKEND_URL}/check_solution/", json={"solution": solution})
    return jsonify(response.json())

@app.route('/new_game', methods=['GET'])
def new_game():
    # Get the difficulty from the request
    difficulty = request.args.get('difficulty', 'easy').lower()

    # Filter games by the selected difficulty
    filtered_games = [game for game in games_data if game["difficulty"] == difficulty]

    # Choose a random game from the filtered list
    if filtered_games:
        game = random.choice(filtered_games)
        return jsonify({"puzzle": game["puzzle"]})
    else:
        return jsonify({"error": "No games found for the selected difficulty"}), 404
'''

from flask import Flask, render_template, request, jsonify
import requests
import json, random

app = Flask(__name__)

# This is where we store the current board and history of moves
HISTORY = []  # Stack to track move history
current_board = []  # 2D array to represent the current Sudoku board

BACKEND_URL = "http://127.0.0.1:8000/sudoku"

# Load the games from the JSON file
with open('games.json') as f:
    games_data = json.load(f)["sudoku_games"]

def flatten_board():
    """Flatten the board to a single list to send to the frontend for rendering."""
    return [item for row in current_board for item in row]

@app.route('/')
def index():
    # Fetch the current puzzle from the backend
    puzzle = requests.get(f"{BACKEND_URL}/get_puzzle/").json()
    global current_board
    current_board = puzzle["puzzle"]  # Initialize the current board with the puzzle
    return render_template('index.html', puzzle=puzzle["puzzle"])

@app.route('/undo', methods=['POST'])
def undo_move():
    print("Attempting to undo. Current move history:", HISTORY)  # Debug

    if HISTORY:
        # Pop the last move from history
        last_move = HISTORY.pop()
        row, col, previous_value = last_move
        current_board[row][col] = previous_value  # Revert the board cell to previous value
        return jsonify({'status': 'success', 'board': flatten_board()})
    else:
        return jsonify({'status': 'error', 'message': 'No moves to undo'})

@app.route('/track_move', methods=['POST'])
def track_move():
    data = request.json
    row = data['row']
    col = data['col']
    new_value = data['value']
    previous_value = current_board[row][col]

    # Only track moves if the new value is different
    if previous_value != new_value:
        # Store the move in history
        HISTORY.append((row, col, previous_value))
        # Update the board with the new value
        current_board[row][col] = new_value

    # Debug: Print the history to verify tracking
    print("Current move history:", HISTORY)

    return jsonify({'status': 'success'})


@app.route('/check_solution', methods=['POST'])
def check_solution():
    solution = request.json.get("solution")
    response = requests.post(f"{BACKEND_URL}/check_solution/", json={"solution": solution})
    return jsonify(response.json())

@app.route('/new_game', methods=['GET'])
def new_game():
    # Get the difficulty from the request
    difficulty = request.args.get('difficulty', 'easy').lower()

    # Filter games by the selected difficulty
    filtered_games = [game for game in games_data if game["difficulty"] == difficulty]

    # Choose a random game from the filtered list
    if filtered_games:
        game = random.choice(filtered_games)
        global current_board, HISTORY
        current_board = game["puzzle"]
        HISTORY = []  # Reset move history when a new game is loaded
        return jsonify({"puzzle": game["puzzle"]})
    else:
        return jsonify({"error": "No games found for the selected difficulty"}), 404

if __name__ == '__main__':
    app.run(debug=True)
