from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

# Define the possible values for a 4x4 Sudoku and the board size
BOARD_SIZE = 4
NUM_PREFILLED_CELLS = 6  # Number of cells to pre-fill on each new board

# Generate an initial empty board
def generate_new_board():
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    fill_random_cells(board)
    return board

def generate_sudoku_board(empty_cells=6):
    # Base valid 4x4 Sudoku board
    base_board = [
        [1, 2, 3, 4],
        [3, 4, 1, 2],
        [2, 1, 4, 3],
        [4, 3, 2, 1]
    ]

    def shuffle_sudoku(board):
        # Shuffle rows within each 2x2 grid
        row_blocks = [0, 1], [2, 3]
        for block in row_blocks:
            rows = list(block)
            random.shuffle(rows)
            board[block[0]], board[block[1]] = board[rows[0]], board[rows[1]]

        # Shuffle columns within each 2x2 grid
        col_blocks = [0, 1], [2, 3]
        for block in col_blocks:
            cols = list(block)
            random.shuffle(cols)
            for row in board:
                row[block[0]], row[block[1]] = row[cols[0]], row[cols[1]]

        return board

    # Shuffle the base board to create a valid but randomized board
    board = shuffle_sudoku(base_board)

    # Flatten the board for easier manipulation
    flat_board = [cell for row in board for cell in row]

    # Randomly remove `empty_cells` number of cells to create the puzzle
    empty_positions = random.sample(range(16), empty_cells)
    for pos in empty_positions:
        flat_board[pos] = 0  # Set the cell to 0 to indicate it's empty

    return flat_board

    
# Fill the board with some random cells for a new puzzle
def fill_random_cells(board):
    positions = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]
    random.shuffle(positions)

    for _ in range(NUM_PREFILLED_CELLS):
        row, col = positions.pop()
        value = random.randint(1, BOARD_SIZE)
        while not is_safe_to_place(board, row, col, value):
            value = random.randint(1, BOARD_SIZE)
        board[row][col] = value

# Check if placing a value at a specific position is valid according to Sudoku rules
def is_safe_to_place(board, row, col, value):
    # Check the row and column
    if value in board[row] or value in [board[r][col] for r in range(BOARD_SIZE)]:
        return False
    
    # Check the 2x2 sub-grid
    start_row, start_col = (row // 2) * 2, (col // 2) * 2
    for i in range(start_row, start_row + 2):
        for j in range(start_col, start_col + 2):
            if board[i][j] == value:
                return False
    return True

# Initialize the current board
current_board = generate_new_board()

@app.route('/')
def index():
    flattened_board = [cell for row in current_board for cell in row]
    return render_template('index.html', board=flattened_board)

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.json
    position = data['position']
    value = int(data['value'])
    
    row, col = divmod(position, BOARD_SIZE)
    if 1 <= value <= BOARD_SIZE:
        current_board[row][col] = value
        return jsonify({'status': 'success', 'board': flatten_board(), 'winner': is_sudoku_solved(current_board)})
    else:
        return jsonify({'status': 'error', 'message': 'Value must be between 1 and 4'})

@app.route('/restart', methods=['POST'])
def restart():
    # Generate a new board here with randomly placed numbers
    new_board = generate_sudoku_board(empty_cells=6)  # Replace with your board generation logic
    return jsonify(board=new_board)
    
@app.route('/check_puzzle', methods=['POST'])
def check_puzzle():
    solved = is_sudoku_solved(current_board)
    return jsonify({'solved': solved})

def is_sudoku_solved(board):
    for row in board:
        if 0 in row:
            return False
    for i in range(BOARD_SIZE):
        if len(set(board[i])) != BOARD_SIZE:
            return False
        if len(set(row[i] for row in board)) != BOARD_SIZE:
            return False
    for x in range(0, BOARD_SIZE, 2):
        for y in range(0, BOARD_SIZE, 2):
            subgrid = {board[x][y], board[x+1][y], board[x][y+1], board[x+1][y+1]}
            if len(subgrid) != BOARD_SIZE:
                return False
    return True

def flatten_board():
    return [cell for row in current_board for cell in row]

if __name__ == '__main__':
    app.run(debug=True)
