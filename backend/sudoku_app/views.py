import json
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Global variable to hold the current puzzle
current_puzzle = None

def load_games():
    with open('../frontend/games.json') as f:
        data = json.load(f)["sudoku_games"]
    return data

def reset_game():
    global current_puzzle
    games = load_games()
    current_puzzle = random.choice(games)

# Initialize the first game when the server starts
reset_game()

@csrf_exempt
def get_current_puzzle(request):
    # Return the current puzzle without changing it
    return JsonResponse(current_puzzle)

@csrf_exempt
def check_solution(request):
    if request.method == "POST":
        user_solution = json.loads(request.body).get("solution")
        # Ensure both the user's solution and backend solution are in the same format
        expected_solution = current_puzzle["solution"]

        # Check if user solution matches the expected solution
        if user_solution == expected_solution:
            return JsonResponse({"status": "correct"})
        else:
            return JsonResponse({"status": "incorrect"})
    return JsonResponse({"status": "error"})

@csrf_exempt
def new_game(request):
    # Set a new random puzzle as the current game
    reset_game()
    return JsonResponse(current_puzzle)
