import json
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sudoku_app.models import SudokuGames
from sudoku_app.models import Sessions
from sudoku_app.models import Cell
from sudoku_app.models import History
from django.shortcuts import render

# Global variable to hold the current puzzle
current_puzzle = None

# Mark
@csrf_exempt # to keep for testing purposes
def index(request):
    sessionsTracker = Sessions.objects.all()
    sessions_data = []

    for session in sessionsTracker:
        # Fetch all cells related to the current session
        cellsTracker = session.cells.all()
        cells_data = list(cellsTracker.values("row", "column", "value", "solution", "pre_filled"))

        # Fetch all history records related to the current session
        historyTracker = History.objects.filter(session=session)
        history_data = list(historyTracker.values("cell__row", "cell__column", "previous_value", "new_value", "timestamp", "correct_move"))

        # Add session data along with its cells
        sessions_data.append({
            "session_id": session.id,
            "sudoku_game_id": session.sudoku_game.id,
            "created_at": session.created_at,
            "last_updated": session.last_updated,
            "cells": cells_data,
            "history": history_data,
        })

    return JsonResponse(sessions_data, safe=False)

# Mark
@csrf_exempt
def get_current_puzzle(request):
    global current_puzzle
    session_id = request.GET.get('session_id')
    if not session_id:
        return JsonResponse({"error": "Session ID is required"}, status=400)
    
    current_session = Sessions.objects.get(id = session_id) # get the current session
    current_puzzle = SudokuGames.objects.get(id = current_session.sudoku_game.id) # get the puzzle associated with the session
    
    cells = current_session.cells.all()  # Retrieve all cells related to this session
    cells_list = []  # List to store the cell information
    
    for cell in cells:
        cell_data = {
            "row": cell.row,
            "column": cell.column,
            "value": cell.value,
            "solution": cell.solution,
            "pre_filled": cell.pre_filled  # True if the cell has a pre-filled value (non-zero)
        }
        cells_list.append(cell_data)  # Add the cell's data to the list

    # Return the current puzzle without changing it
    if current_puzzle:
        return JsonResponse({
            "puzzle_id": current_puzzle.id,
            "cells": cells_list,  # Return the list of cells instead of the puzzle grid
            "solution": current_puzzle.solution,
            "difficulty": current_puzzle.difficulty,
            "size": current_puzzle.size
        })
    else:
        return JsonResponse({"error": "No puzzle available"})

# Mark
@csrf_exempt
def new_session(request):
    global current_puzzle
    games = SudokuGames.objects.filter(size = 4, difficulty = "easy") 
    current_puzzle = random.choice(games)
    
    # Create a new session for the first game
    session = Sessions.objects.create(sudoku_game=current_puzzle) # relates a random game to the new session
    
    # Initialize cells for the session
    for row_index, row in enumerate(current_puzzle.puzzle):
        for col_index, value in enumerate(row):
            # Check if the cell's value is non-zero (pre-filled)
            pre_filled = value != 0  # True if the cell is pre-filled
            
            # Create the cell with the pre_filled flag set accordingly
            Cell.objects.create(
                session=session,
                row=row_index,
                column=col_index,
                value=value,
                solution=current_puzzle.solution[row_index][col_index],
                pre_filled=pre_filled  # Set pre_filled to True if the value is non-zero
            )

    # Return the session id and puzzle information
    if current_puzzle:
        return JsonResponse({
            "session_id": session.id,
            "puzzle_id": session.sudoku_game.id,
            "puzzle": session.sudoku_game.puzzle,
            "solution": session.sudoku_game.solution,
            "difficulty": session.sudoku_game.difficulty,
            "size": session.sudoku_game.size
        })
    else:
        return JsonResponse({"error": "No puzzle available"})
    
""" @csrf_exempt
def check_solution(request):
    if request.method == "POST":
        user_solution = json.loads(request.body).get("solution")
        # Ensure both the user's solution and backend solution are in the same format
        expected_solution = current_puzzle.solution

        # Check if user solution matches the expected solution
        if user_solution == expected_solution:
            return JsonResponse({"status": "correct"})
        else:
            return JsonResponse({"status": "incorrect"})
    return JsonResponse({"status": "error"}) """

# Mark
@csrf_exempt
def new_game(request):
    # Extract query parameters with default values
    difficulty = request.GET.get('difficulty', 'easy').lower()
    size = int(request.GET.get('size', 4))  # Default to 4 if not provided

    # identify old session id
    existing_id = request.GET.get('session_id', 0) # Pass session_id from the frontend, default to 0 if not

    # Check for an existing session and delete it
    if existing_id != 0:
        existing_sessions = Sessions.objects.filter(id=existing_id)
        if existing_sessions.exists():
            existing_sessions.delete()
    
    # Filter games from the database based on difficulty and size
    filtered_games = SudokuGames.objects.filter(difficulty=difficulty, size=size)

    # Check if any games match the criteria
    if filtered_games.exists():
        # Randomly select a game from the filtered list
        selected_game = random.choice(filtered_games)

        # Create a new session for the selected game
        session = Sessions.objects.create(sudoku_game=selected_game)
        
        global current_puzzle
        current_puzzle = selected_game  # Update the current puzzle to the newly selected one
        
        cells_list = []  # List to store the cell information

        # Initialize cells for the session
        for row_index, row in enumerate(current_puzzle.puzzle):
            for col_index, value in enumerate(row):
                # Check if the cell's value is non-zero (pre-filled)
                pre_filled = value != 0  # True if the cell is pre-filled
            
                # Create the cell with the pre_filled flag set accordingly
                cell = Cell.objects.create(
                    session=session,
                    row=row_index,
                    column=col_index,
                    value=value,
                    solution=current_puzzle.solution[row_index][col_index],
                    pre_filled=pre_filled  # Set pre_filled to True if the value is non-zero
                )
                # Add the cell data directly to the cells_data list
                cells_list.append({
                    "row": cell.row,
                    "column": cell.column,
                    "value": cell.value,
                    "solution": cell.solution,
                    "pre_filled": cell.pre_filled
                })

        return JsonResponse({
            "session_id": session.id,
            "puzzle": selected_game.puzzle,
            "cells": cells_list,
            "solution": selected_game.solution,
            "difficulty": selected_game.difficulty,
            "size": selected_game.size
        })
    else:
        # Return an error if no matching games are found
        return JsonResponse({
            "error": f"No games found for difficulty '{difficulty}' and size {size}."
        }, status=404)

#Jonathan
@csrf_exempt
def is_correct(request):
    data = json.loads(request.body)  
    user_row = int(data.get("row"))  # Convert to integer
    user_col = int(data.get("col"))  # Convert to integer
    session_id = int(data.get("session_id"))
    user_value = int(data.get("userValue"))
    
    session = Sessions.objects.get(id = session_id) # get the current session
    
    # Fetch the cell from the database
    cell = Cell.objects.filter(session=session, row=user_row, column=user_col).first()
    if not cell:
        return JsonResponse({"error": "Cell not found"}, status=404)
    
    # Check if the user value is correct
    correct = current_puzzle.solution[user_row][user_col] == user_value

    # Get the corresponding history record
    history_entry = History.objects.filter(session=session, cell=cell).first()
    if history_entry:
        # Update the `correct_move` field
        history_entry.correct_move = correct
        history_entry.save()  # Save the updated history entry
    
    # Return the result
    return JsonResponse({"correct": correct})

# Mark   
@csrf_exempt
def get_history(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        return JsonResponse({"error": "Session ID is required"})

    try:
        session = Sessions.objects.get(id=session_id)
        history_records = session.history.all().order_by("-timestamp")  # Get history related to the session

        # Serialize history records
        history_data = [
            {
                "cell": {
                    "row": record.cell.row,
                    "column": record.cell.column
                },
                "previous_value": record.previous_value,
                "new_value": record.new_value,
                "timestamp": record.timestamp,
                "correct_move": record.correct_move
            }
            for record in history_records
        ]

        return JsonResponse({"history": history_data})
    except Sessions.DoesNotExist:
        return JsonResponse({"error": "Session not found"}, status=404)

#Jonathan
@csrf_exempt
def update_history(request):
    session_id = request.GET.get("session_id")
    session = Sessions.objects.get(id=session_id)
    if not session_id:
        return JsonResponse({"error": "Session ID is required"}, status=400)
    try: 
        data = json.loads(request.body)
        incoming_history = data.get("history")

        if not incoming_history:
            return JsonResponse({"error": "Missing 'history' field in the request"}, status=400)

        # Clear existing history for the session
        session.history.all().delete()

        # Create new History entries using bulk_create
        history_instances = [
            History(
                session=session,
                cell=Cell.objects.get(
                    session=session,
                    row=record["cell"]["row"],
                    column=record["cell"]["column"],
                ),
                previous_value=record.get("previous_value", 0),
                new_value=record["new_value"],
            )
            for record in incoming_history
        ]

        # Bulk create the new history entries
        History.objects.bulk_create(history_instances)

        return JsonResponse({"success": True, "message": "History updated successfully"})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
# Mark
@csrf_exempt
def update_cell(request):
   # if request.method == "POST":
        data = json.loads(request.body)
        session_id = data.get("session_id")
        row = data.get("row")
        column = data.get("column")
        new_value = data.get("new_value")

        if not session_id or row is None or column is None or new_value is None:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        try:
            # Retrieve the session and cell
            session = Sessions.objects.get(id=session_id)
            cell = Cell.objects.get(session=session, row=row, column=column)
            correct = (new_value == cell.solution)

            # Record the history
            History.objects.create(
                session=session,
                cell=cell,
                previous_value=cell.value,
                new_value=new_value,
                correct_move = correct
            )

            # Update the cell's value
            cell.value = new_value
            cell.save()

            return JsonResponse({"success": True, "message": "Cell updated successfully"})
        except Sessions.DoesNotExist:
            return JsonResponse({"error": "Session not found"}, status=404)
        except Cell.DoesNotExist:
            return JsonResponse({"error": "Cell not found"}, status=404)
    #return JsonResponse({"error": "Invalid request method"}, status=405)

#Jonathan
@csrf_exempt
def reset_cell(request):
    data = json.loads(request.body)
    session_id = data.get("session_id")
    row = data.get("row")
    column = data.get("column")
    new_value = 0
    try:
        # Retrieve the session and cell
        session = Sessions.objects.get(id=session_id)
        cell = Cell.objects.get(session=session, row=row, column=column)

        # Update the cell's value
        cell.value = new_value
        cell.save()

        return JsonResponse({"success": True, "message": "Cell updated successfully"})
    except Sessions.DoesNotExist:
        return JsonResponse({"error": "Session not found"}, status=404)
    except Cell.DoesNotExist:
        return JsonResponse({"error": "Cell not found"}, status=404)
    
#Jonathan
@csrf_exempt
def set_note(request):
    try:
        data = json.loads(request.body)
        session_id = data.get("session_id")
        note = data.get("note_value")
        row = data.get("row")
        column = data.get("column")
        session = Sessions.objects.get(id=session_id)
        cell = Cell.objects.get(session=session, row=row, column=column)
        cell.notes.append(int(note))
        return JsonResponse({"success": True, "message": "Notes updated successfully"})
    except Sessions.DoesNotExist:
        return JsonResponse({"error": "Session not found"}, status=404)
    except Cell.DoesNotExist:
        return JsonResponse({"error": "Cell not found"}, status=404)

#Jonathan
@csrf_exempt
def get_notes(request):
    try:
        data = json.loads(request.body)
        session_id = data.get("session_id")
        note = data.get("note_value")
        row = data.get("row")
        column = data.get("column")
        session = Sessions.objects.get(id=session_id)
        cell = Cell.objects.get(session=session, row=row, column=column)
        notes = cell.notes
        return JsonResponse({"notes": notes})
    except Sessions.DoesNotExist:
        return JsonResponse({"error": "Session not found"}, status=404)
    except Cell.DoesNotExist:
        return JsonResponse({"error": "Cell not found"}, status=404)