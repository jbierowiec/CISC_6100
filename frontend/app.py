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

@app.route('/')
def index():
    # Fetch the current puzzle from the backend
    puzzle = requests.get(f"{BACKEND_URL}/get_puzzle/").json()
    global current_board
    current_board = puzzle["puzzle"]  # Initialize the current board with the puzzle
    return render_template(
        'index.html',
        puzzle=puzzle["puzzle"],
        solution=puzzle["solution"]  # Pass the solution to the template
    )

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
        return jsonify({
            "puzzle": game["puzzle"],
            "solution": game["solution"]
        })
    else:
        return jsonify({"error": "No games found for the selected difficulty"}), 404

if __name__ == '__main__':
    app.run(debug=True)
