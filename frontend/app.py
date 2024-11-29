from flask import Flask, render_template, request, jsonify
import requests
import json, random

app = Flask(__name__)

# This is where we store the current board and history of moves
HISTORY = []  # Stack to track move history
current_board = []  # 2D array to represent the current Sudoku board

BACKEND_URL = "http://127.0.0.1:8000/sudoku"

# Jonathan
# HISTORY will be a list of moves with this data
class Move:
    def __init__(self, row, col, value, correct):
        self.row = row
        self.col = col
        self.value = value
        self.correct = correct

    def __repr__(self):
        return f"Move(row={self.row}, col={self.col}, value={self.value}, correct={self.correct})"

# Jan
@app.route('/')
def index():
    return render_template('index.html')

# Mark
@app.route('/get_puzzle', methods = ['GET'])
def get_puzzle():
    session_id = request.args.get('session_id')
    # gets the puzzle that was associates with the given session
    puzzle = requests.get(f"{BACKEND_URL}/get_puzzle/", params={ "session_id": session_id}).json()
    return jsonify({
        "puzzle": puzzle["puzzle"], # return the puzzle from the backend response
        "solution": puzzle["solution"]  
    })

# Mark
@app.route('/get_session', methods = ['GET'])
def get_session():    
    current_session_id = request.args.get('session_id') 
    if (current_session_id == '0'):
        new_session= requests.get(f"{BACKEND_URL}/new_session/").json()
        return jsonify({"new_session_id": new_session["session_id"]})
    else:
        return jsonify({"new_session_id": current_session_id})

# Jan
@app.route('/check_solution', methods=['POST'])
def check_solution():
    solution = request.json.get("solution")
    response = requests.post(f"{BACKEND_URL}/check_solution/", json={"solution": solution})
    return jsonify(response.json())

# Jan
@app.route('/new_game', methods=['GET'])
def new_game():
    # Get the difficulty from the request
    difficulty = request.args.get('difficulty', 'easy').lower()
    
    # Get the size from the request, default to 4x4 if not provided
    size = int(request.args.get('size', 4))

    session_id = request.args.get('session_id', 0)  # Get the session_id if it exists (from the frontend), 

    # Pass the session_id to the backend, where the session will be deleted
    puzzle_data = requests.get(
        f"{BACKEND_URL}/new_game/", 
        params={"difficulty": difficulty, "size": size, "session_id": session_id}
    ).json()
    
    global current_board, HISTORY
    current_board = puzzle_data["puzzle"]  # Update the current board
    HISTORY = []  # Reset move history for the new game
    return jsonify({
        "puzzle": puzzle_data["puzzle"],
        "session_id": puzzle_data["session_id"]  # Return the session_id from the backend response
    })

# Jan
@app.route('/get_hint', methods=['POST'])
def get_hint():
   data = request.json
   row = data.get("row")
   col = data.get("col")

   if row is None or col is None:
       return jsonify({"error": "Invalid row or column"}), 400

   try:
       hint_value = current_solution[row][col]
       return jsonify({"hint": hint_value})
   except IndexError:
       return jsonify({"error": "Invalid cell position"}), 400

# Jonathan
@app.route('/isCorrect', methods=['POST'])
def isCorrect():
    row = request.json.get("row")
    col = request.json.get("col")
    userValue = request.json.get("value")
    response = requests.post(f"{BACKEND_URL}/is_correct/", json={"row": row, "col": col, "userValue": userValue})
    response_data = response.json()
    isCorrect = response_data.get("correct")
    move = Move(int(row), int(col), int(userValue), isCorrect)
    current_board[move.row][move.col] = move.value
    HISTORY.append(move)
    return jsonify(response.json())

# Jonathan
@app.route('/undoUntilCorrect', methods=['POST'])
def undoUntilCorrect():
    global HISTORY
    first_wrong = len(HISTORY) + 1
    # Find the index of the first incorrect move
    for index, move in enumerate(HISTORY):
        if not move.correct:
            first_wrong = index
            break

    # Reset the spots on the board for moves after the first_wrong index
    for index in range(first_wrong, len(HISTORY)):
        move = HISTORY[index]
        current_board[move.row][move.col] = 0  # Reset the spot to 0

    # Keep only the moves up to the first_wrong index in HISTORY
    HISTORY = HISTORY[:first_wrong]

    print(current_board)

    return jsonify({
        "puzzle": current_board,
        "index": first_wrong
    })

        
if __name__ == '__main__':
    app.run(debug=True)
