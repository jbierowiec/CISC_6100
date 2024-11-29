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

@csrf_exempt # to keep for testing purposes
def index(request):
    sessionsTracker = Sessions.objects.all()
    sessions_data = []

    for session in sessionsTracker:
        # Fetch all cells related to the current session
        cellsTracker = session.cells.all()
        cells_data = list(cellsTracker.values("row", "column", "value", "solution"))

        # Add session data along with its cells
        sessions_data.append({
            "session_id": session.id,
            "sudoku_game_id": session.sudoku_game.id,
            "created_at": session.created_at,
            "last_updated": session.last_updated,
            "cells": cells_data,
        })

    return JsonResponse(sessions_data, safe=False)

@csrf_exempt
def get_current_puzzle(request):
    global current_puzzle
    session_id = request.GET.get('session_id')
    if not session_id:
        return JsonResponse({"error": "Session ID is required"}, status=400)
    
    current_session = Sessions.objects.get(id = session_id) # get the current session
    current_puzzle = SudokuGames.objects.get(id = current_session.sudoku_game.id) # get the puzzle associated with the session
    
    # Return the current puzzle without changing it
    if current_puzzle:
        return JsonResponse({
            "puzzle_id": current_puzzle.id,
            "puzzle": current_puzzle.puzzle,
            "solution": current_puzzle.solution,
            "difficulty": current_puzzle.difficulty,
            "size": current_puzzle.size
        })
    else:
        return JsonResponse({"error": "No puzzle available"})

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
            Cell.objects.create(
                session=session,
                row=row_index,
                column=col_index,
                value=value,
                solution=current_puzzle.solution[row_index][col_index]
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
    
@csrf_exempt
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
    return JsonResponse({"status": "error"})

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
        
        # Initialize cells for the session
        for row_index, row in enumerate(selected_game.puzzle):
            for col_index, value in enumerate(row):
                Cell.objects.create(
                    session=session,
                    row=row_index,
                    column=col_index,
                    value=value,
                    solution=selected_game.solution[row_index][col_index]
                )

        return JsonResponse({
            "session_id": session.id,
            "puzzle": selected_game.puzzle,
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
    data = json.loads(request.body)  # Define 'data'
    user_row = int(data.get("row"))  # Convert to integer
    user_col = int(data.get("col"))  # Convert to integer
    user_value = json.loads(request.body).get("userValue")
    if(current_puzzle.solution[user_row][user_col] == user_value):
        return JsonResponse({
            "correct": True
        })
    else:
        return JsonResponse({
            "correct": False
        })