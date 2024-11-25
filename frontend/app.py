from flask import Flask, render_template, request, jsonify
import requests
import json, random

app = Flask(__name__)

# This is where we store the current board and history of moves
HISTORY = []  # Stack to track move history
current_board = []  # 2D array to represent the current Sudoku board

BACKEND_URL = "http://127.0.0.1:8000/sudoku"

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
    
    # Get the size from the request, default to 4x4 if not provided
    size = int(request.args.get('size', 4))

    # request for a new puzzle based on the selected difficulty/size
    puzzle_data = requests.get(f"{BACKEND_URL}/new_game/", params={"difficulty": difficulty, "size": size}).json()
    
    global current_board, HISTORY
    current_board = puzzle_data["puzzle"]  # Update the current board
    HISTORY = []  # Reset move history for the new game
    return jsonify({"puzzle": puzzle_data["puzzle"]})
        
if __name__ == '__main__':
    app.run(debug=True)
