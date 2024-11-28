import json
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sudoku_app.models import SudokuGames
from sudoku_app.models import Sessions
from django.shortcuts import render

# Global variable to hold the current puzzle
current_puzzle = None

@csrf_exempt # to keep for testing purposes
def index(request):
    sessionsTracker = Sessions.objects.all()
    sessions_data = list(sessionsTracker.values())  # Convert queryset to a list of dictionaries
    return JsonResponse(sessions_data, safe=False)

@csrf_exempt
def get_current_puzzle(request):
    global current_puzzle
    games = SudokuGames.objects.all() # sets to all games in the database
    current_puzzle = random.choice(games)
    
    # Create a new session for the first game
    session = Sessions.objects.create(sudoku_game=current_puzzle)
    
    # Return the current puzzle without changing it
    if current_puzzle:
        return JsonResponse({
            "session_id": session.id,
            "puzzle_id": current_puzzle.id,
            "puzzle": current_puzzle.puzzle,
            "solution": current_puzzle.solution,
            "difficulty": current_puzzle.difficulty,
            "size": current_puzzle.size
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