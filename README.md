# CISC 6100 Software Engineering Sudoku Project

This repository contains the source code for the Software Engineering Sudoku Game Project. The application is built using Flask for the frontend and Django for the backend, with the website designed to be dynamic and responsive using HTML and CSS, ensuring compatibility with both personal computers and mobile devices. The database that stores all the sudoku games is a SQLite database.

## Full Stack Digram 

![Full Stack Diagram](diagrams/FullStack%20Diagram.png)

---

## Overview

The Sudoku Game Project is a web-based application that provides users with a unique Sudoku experience. Users can select the game difficulty, board size, switch between light and dark mode, track their game progress with an integrated timer, and interact with the game through its numerous buttons, featuring the: Undo, Undo Until Correct, Get Specifc Hint, Get Random Hint, Check Solution, Create New Game, Set Note and the Clear Note buttons. 

## Story Board Diagram

Here are our story board of how we envisioned for the Sudoku game to look like, as well as the in game play features:

![Story Board of a 4x4 Sudoku Game](diagrams/Story%20Board%204x4.png)

![Story Board of a 9x9 Sudoku Game in play](diagrams/Story%20Board%209x9%20Game%20Play.png)

---

## Project Structure

```plaintext
├── backend
│   ├── backend
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   ├── sudoku_app
│   │   ├── __pycache__/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
│   ├── db.sqlite3
│   └── manage.py
├── frontend
│   ├── __pycache__/
│   ├── static
│   │   └── style.css
│   ├── templates
│   │   └── index.html
└── app.py
```

## Database 
  - **Sudoku Games**: This includes pre-made Sudoku games with varying levels of difficulty, sizes, as well as solutions. 
  - **Sessions**: This includes the ability for there to be multiple sessions or instances of the same game to be running on a different browser with a uniquey generated ID
  - **Cells**: A method of storing information about a cell, whether it was a prefilled (generated) cell, and empty cell, where the cell is located with respect to the entire board grid, the value that it has, the solution for all the empty cells as well as an ability to enter notes on a cell
  - **History**: This includes information about a session, a value that is entered into an empty cell, previous values entered into previously entered cells, a timestamp of when moves are made, as well as a flas that determines if a move made by the user is correct or not.
  - **Notes**: This allows the user to enter multiple values into any given empty cell in such a way that the value is smaller than the rest and it can be cleared. 

![Database Schema](diagrams/Database_Schema_by_Mark.jpg)

## Features

### Light and Dark Mode
- **Toggle Button**: A "Light/Dark Mode" button allows users to switch between light and dark themes, enhancing the user interface and user experience.

### Timer Functionality
- **Automatic Reset**: The timer resets each time the user clicks on the "Create New Game" button, or when a game is lost causing a generation of a new game
- **Auto-Stop on Completion**: The timer stops when the user correctly solves the Sudoku puzzle, or when the user makes three mistakes, causing them to lose the game.
- **Pause on Inactivity**: The timer pauses whenever the user switches to another browser tab or clicks the "Check Solution" button.

### Difficulty Dropdown
- **Difficulty Selection**: Users can select a difficulty level (Easy, Medium, Hard) from a dropdown menu.
- **Dynamic Game Generation**: Based on the selected difficulty, the app generates a new game. For example:
  - If "Easy" is selected, only 4x4, 9x9, or 16x16 easy games are displayed.
  - If "Medium" is selected, only 4x4, 9x9, or 16x16 medium games are displayed.
  - If "Hard" is selected, only 4x4, 9x9, or 16x16 hard games are displayed.

### Size Dropdown
- **Size Selection**: Users can select a game board size (4x4, 9x9, 16x16) from a dropdown menu.
- **Dynamic Game Generation**: Based on the selected size, the app generates a new game. For example:
  - If "4x4" is selected, only 4x4 easy, medium and hard games are displayed.
  - If "9x9" is selected, only 9x9 easy, medium and hard games are displayed.
  - If "16x16" is selected, only 16x16 easy, medium and hard games are displayed.

### Generate New Game Button
- **Difficulty-Based and Size-Based Game Selection**: The "Generate New Game" button fetches games from a `db.sqlite3` file based on the user's choice of the game's difficulty and game board size.

### Check Solution Button
- **Validation Against Stored Solutions**: Each Sudoku game is pre-generated and stored in a `db.sqlite3` file, including the solution, as well as all the other features mentioned in the Database Section. When the user clicks "Check Solution," the system verifies if the user’s inputs match the correct solution from the backend.

### Undo Button
- The user can press can click on the Undo Button any time a move is made, and because moves are recorded in the history on the backend, if a user presses this button, the move that was previously made by the user is removed and set to be a blank cell again. This works in such a way that most recent number will be popped from the user input history (Last In First Out).

### Undo Until Correct Button
- The user can press this button at any point in the game and it will work in a such a way, that all the user's moves are stored and recorded to be either correct or incorrect moves. The Undo Until Correct button will search through the game's history and find the very first incorrect value inputted by the user and making sure that all the moves prior to the incorrect move are all correct. For example:
  - If the very first move made by the user is incorrect, every move will be cleared.
  - If the user made three correct moves followed by two incorrect moves, the two incorrect moves will be removed ant the three correct moves will remain displayed
  - If the user made a correct, correct, incorrect, correct, incorrect set of moves, the two incorrect moves, as well as the correct move in between the two incorrect moves will be removed. Leaving only the original two correct moves. 

### Get Specific Hint Button
- The user can click this button at any point during the game. The user first specifies the empty cell they would like to get a hint for, and then the correct value for that given cell's row and column will be provided and will be autofilled for the user. 

### Get Random Hint Button
- The user can click this button at any point during the game. In contrast to the get specific hint button, the user does not specify any cell, but clicks this button directly, mid-game. When clicking this button thw following two things can occur:
 - If all moves by the user are correct, an empty cell is found at random and is filled in by the game
 - Otherwise if a user made an incorrect value, that incorrect value is identified by the program, it is removed and replaced by the correct value that should be in that given cell. 

### Set Note Button
- When this button is clicked on, this allows the user to enter more than one value in such a way that the values are a smaller font size that the regular game size numbers, and these noted numbers are potential candidates for whether or not that number should be inputted into that given cell. When this mode is on, any every empty cell is allowed to have more than one value. If it is off, then the user is only allowed to enter one value per cell as by the game rules logic.

### Clear Note Button
- When the user is sure of inputting a specific value into a previously noted cell, the user then clicks this button, which removes all the notes made in a cell, allowing the user to now enter a single value into that cell. 

### Number Buttons
- If the user clicks on a Number Button without first clicking a empty cell, a message will show up on the screen, notifying the user that they should select an empty cell first.
- If the user clicks an empty cell, and then clicks on any number, that number will be filled in the specific cell that the user previously clicked on.

### Error Flags
- If the user enters any value in a cell where the row, column, or 2x2, 3x3, or 4x4 square (depending on the game board size) contains that same value, the cells where there are duplicates will turn red indicating an error in sudoku logic, meaning the user will have to input a different value in order to proceed in continuing the sudoku game.
- If the user makes three such mistakes in the game, a message box will come up notifying the user that they have lost the game, displaying a 10 second timer that decerements down. Once complete, a new game is loaded onto the scree.
- If the user has incorreclty inputted values in the game, and they click on the "Check Solution" button, they will be notified that their inputed are incorrect. 

### Use Case Diagram

![General Use Case Diagram](diagrams/High%20Level%20Use%20case%20diagram.png)

### Activity Diagram

![Validating a Value Activity Diagram](diagrams/Validating%20a%20Value.png)

![Undo Until Correct Activity Diagram](diagrams/Activity%20diagram%20UndoTillCorrect.png)

### Sequence Diagram

![Undo Sequence Diagram](diagrams/Sequence%20diagram%20Undo%20By%20Mark.jpg)

---

## Setup Instructions

To start the backend and frontend servers, follow these steps:

1. **Backend**:
   - Open a terminal, navigate to the `backend` directory:
     ```bash
     cd backend
     ```
   - Start the Django backend server:
     ```bash
     python manage.py runserver
     ```

2. **Frontend**:
   - Open a second terminal, navigate to the `frontend` directory:
     ```bash
     cd frontend
     ```
   - Start the Flask frontend server:
     ```bash
     python app.py
     ```

3. **Alternative Setup**:
   - In the `past_github_upload` directory, you can run the program directly:
     ```bash
     cd past_github_upload
     python app.py
     ```

---

## Changes Made
- Originally most of the buttons fetched data from a `games.json` file. Since then, the code has been refactored in considering multiple games running in different sessions, as well as optimizing the database, the data is now fetched from a `db.sqlite3` file. This decision was made due to SQLite being a better data model to store our games, as well as it allowing for seamless Backend and Frontend communication. 
- Original functions that were related to the `games.json` file have either been deleted or adjusted accordingly when the refactoring process was done. 

---

## Testing 
- We have done the following tests during the course of the project:
  **Unit Testing:** We tested individual functions or components to ensure they behave as expected. For example: 
  - We validated the sudoku grid via enforcing row, column, and subgrid uniqueness.
  - We tested the undo and undo until correct buttons to see if the incorrect moves would be popped.
  - We validated the get hint button, through extracting the correct value from the game solution. 
  - These tests were run Using `pytest` or `unittest` 
  **API Testing:** We tested proper requests and communication from the frontend and backend
  - We used this for validating new sessions being created when a new game is played and if the same game is played under two different browsers
  - We validated backend and frontend communication for the check solution, get hint, and undo button functionalities
  - We used Postman for this in order to execute HTTP request to get the desired API responses from the Django server
  **Database Testing:** We validated the integrity and performance of database operations.
  - We ensured proper storage and retrieval of puzzles and user progress.
  - We also tested for data consistency during concurrent sessions.
  - We used `pytest-django` or `pytest-flask` to test database interactions.

## Test Plan (Found in tests.py | can be run by navigating to cd backend and entering python manage.py test |)
Model Testing: We tested the functionality and integrity of the models in the application.

  - We validated the creation of SudokuGames and Cell objects, ensuring that attributes like difficulty, size, solution, and pre-filled status are correctly
    stored in the database.
  - We ensured that each model interacts properly with the database, confirming the correct creation and storage of game data and cells.
  - We used Django’s built-in TestCase class to run these tests and verify model behavior.
  - View Testing: We tested the proper behavior of the views and their responses to different user inputs.

  - We validated the new_game and is_correct views, ensuring that the correct status codes are returned based on the request parameters.
  - We tested if the views properly handle requests from the frontend, such as starting a new game and checking if a solution is correct.
  - We used Django’s test client to simulate HTTP requests and check the responses returned from these views.
  - URL Routing Testing: We validated the proper resolution of URLs to their respective views.

  - In addition, in views.py, the index function actively displays each sessions puzzle, cell values, and history on a backend page. As a player makes moves on        the frontend, you can refresh the backend page to check if the values are being updated correctly.

We confirmed that the URLs for the new_game and is_correct views correctly map to the intended view functions.
We used Django’s reverse and resolve functions to ensure that each URL is connected to the correct view handler.
---

## Individual Contributions
- We all tweaked most parts of the code at some point, but here is what we were each primarily responsible for developing the Sudoku Game:
  - Mark:
    - Did most work primarily in the `views.py`, `models.py`, and `urls.py` files all located under the `backend` directory.
    - Implemented the display of the varying sizes and difficulty of the game board when the games were stored in the `games.json` file.
    - Transfered the the data to a `db.sqlite3` database. 
    - Implemented the entities that are stored in the `models.py` file. 
    - Altered functions along with Jonathan that were originally created by Jan.
    - Implemented the get game, get current puzzle, new session, new game, get history, update cell, and undo requests.
    - Created the database schema diagram as well as the activity diagram for the undo function in the `diagrams` directory.
  - Jan: 
    - Did most work primarily in the `index.html` file, `styles.css` file, and `app.py` file all located under the `frontend` directory, as well as the `test.py` file located under the `backend` directory.
    - Initialized the project creating the GitHub repository, deciding on the Flask & Django framework.
    - Created the original database `games.json` file which was moved to the `past_github_upload` directory, for backup purposes.
    - Created and implemented the remaining timer functionality relating to pausing the game, stoping and resuming.
    - Implemented the features on most of the game, such as the mistake counter, fixing a cell to only have one value, dispalying the lose game screen, a win game screen, as well as validate board function based on user inputs.
    - Implemented the select number buttons, get new game, select number, check solution, undo, get hint, get specific hint, note, update note, and update grid functions, which were also added to by Mark & Jonathan during the refactoring phase.
    - Implemented the UI using CSS as well as made sure the game was relatively responsive and the UI components worked properly
    - Implemented the `test.py` file in order to validate things like creating a Sudoku Game or simulating HTTP requests.
    - Created most diagrams listed in the `diagrams` directory.
  - Jonathan: 
    - Did most work primarily in the `index.html` file, `app.py`, `views.py`, files all located under the `frontend` & `backend` directories.
    - Created and debugged notes functionality, including setting, clearing, and displaying notes. 
    - Implemeted backend route /isCorrect to verify if a move is correct when it is made. 
    - Began work for the timer. 
    - Reworked the check solution and hint functions in the front and backend. 
    - Added a route to the backend to clear history data for a cell. 
    - Began work on the undo/undo untill correct, though I later pivoted away from that and it was reworked/added to by Mark. 

---

# Previously Documented Work Throughout the Project Semester

## Notes
- The games are stored in `games.json` and contain information on each game's grid layout, solutions, and difficulty level.
- Currently, selecting the correct puzzle on the frontend may require manually matching the backend puzzle. This neeeds to fixed for proper frontend to backend communication.
- We now need to try to a few (7 probably) 9x9 sudoku games (3 easy, 2 medium, 2 hard) (to test if the difficulty levels will work if we switch toggles between difficulty levels and size of grid). We also need to adjust the current functionality that works for 4x4 grids to now work for 9x9 grids, and make sure that when 9x9 grids are selected, a 9x9 grid is displayed, replacing the 4x4 grid and vice versa.
- We need to implement buttons for: Undo Until Correct, Generate Random Hint, Generate Specific Hint, Set Note Mode Off/On, Show Solution
- Once evrything is fixed, implemented and the whole system is working, we can then add more functionality if needed, and we need to think about setting up a login system for individual users, other potential pages, like a settings page, etc.

## To Do List
1. ~~Light/Dark Mode Toggle Implemented~~
2. ~~Timer Implemented~~
3. ~~Generate New Game Button Implemented~~
4. ~~Check Solution Button Implemented~~
5. ~~Undo Button Implemented~~
6. ~~Number Buttons Implemented~~
7. ~~Difficulty Dropdown Button Implemented~~
8. ~~Entering a number that is duplicated in the same row/column or 2x2 square warning~~
9. ~~Database with 9x9 and 16x16 grids~~
10. ~~Sudoku Board Size Dropdown Button~~
11. ~~Display of Different Sudoku Grids on Screen~~
12. ~~Generalized Buttons to work for any Grid Size~~
13. ~~Undo Until Correct Button~~
14. ~~Generate Random Hint Button~~
15. ~~Generate Specific Hint Button~~
16. ~~Set Note Mode Off/On Button~~
17. ~~Show Solution Button~~
18. ~~Proper Backend Communication with Frontend~~
19. ~~Separate Game Sessions~~
20. ~~Lose Game Page~~


## Description of Implementations
- Undo Until Correct Button (takes away all wrong number inputs until it reaches the cells with only correct number inputs and preset values)
- Generate Random Hint Button (user clicks the button at anytime, and a empty cell is filled with a value from the solutions part of the JSON file)
- Generate Specific Hint Button (user clicks on an empty cell, then the user clicks on the Get Specific Hint Button and a value is filled in from the solutions part of the JSON file)
- Set Note Button (user clicks on this button, can fill a cell with 4 values for 4x4 sudoku or 9 values for 9x9 sudoku. Those values should all be within a single cell and should have a 2x2 layout for 4x4 sudoku or a 3x3 layout for 9x9 sudoku. If a user inputs a value in a cell that is in the same row or column of the noted cell, then the noted cell should pop the value that was noted, since the value is now used in a different cell. The values inside of the note cell should have those values in a cell in a small font)
- Show Solution Button (user does not want to solve the Sudoku game anymore and want to see the solution)
- Include 3 easy 9x9 sudoku games, 2 medium 9x9 sudoku games, 2 hard 9x9 sudoku games in the JSON file (can be changed later on to be a sqllite3.db)
- Dropdown button for the user to choose the sudoku game size, and for the corresponding grid to display and for the buttons to pull the properly sized games from the JSON file Sudoku game stored games
- Display of the 9x9 sudoku board game and vice versa 4x4 grid based on the user's choice of size from the Dropdown Button
- Make sure the functions become generalized to work for a 4x4 and a 9x9 grid
- Home page where the user enters their name and also clicks on a size and difficulty. They should then be redirected to the game page (don't just have one game page with all the buttons and user choices there)
- Generate New Game button reloads the Backend to include that specifc game so that the Check Solution Button will work along with all other buttons
- The HTML file is currently 700 lines long with the combination of HTML and JavaScript on the file, for better file structure, it would be better to create a separate JavaScript file containing the functionality and separate directory for the index and game pages when both pages are implemented

---
