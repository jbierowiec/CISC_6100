from django.db import models

# Create your models here.

# Mark
class SudokuGames(models.Model):
    puzzle = models.JSONField()
    solution = models.JSONField()
    difficulty = models.CharField(max_length=50)
    size = models.IntegerField()

    def __str__(self):
        return f"{self.difficulty} {self.size}x{self.size} Sudoku"

# Mark   
class Sessions(models.Model): 
    sudoku_game = models.ForeignKey(SudokuGames, on_delete=models.CASCADE, related_name="sessions")
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.session_id} for {self.sudoku_game}"

# Mark
class Cell(models.Model):
    session = models.ForeignKey(Sessions, on_delete=models.CASCADE, related_name="cells")
    row = models.IntegerField()
    column = models.IntegerField()
    value = models.IntegerField(default=0) # value the user has entered for the cell at this position, unspecific values are 0
    solution = models.IntegerField() # solution for the cell at this position
    pre_filled = models.BooleanField(default = False) # whether a cell is supposed to be given or not
    notes = models.JSONField(default=list) #Jonathan - refactored db to make notes part of a cell's data

    def __str__(self):
        return f"Cell ({self.row}, {self.column}) in Session {self.session.id}"

# Mark
class History(models.Model):
    session = models.ForeignKey(Sessions, on_delete=models.CASCADE, related_name="history")
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE, related_name="history")
    previous_value = models.IntegerField()  # The cell's value before the move
    new_value = models.IntegerField()       # The cell's value after the move
    timestamp = models.DateTimeField(auto_now_add=True)  # When the move was made
    correct_move = models.BooleanField(default = False) # if this move led to a correct solution or not

    def __str__(self):
        return (
            f"Move in Session {self.session.id}: Cell ({self.cell.row}, {self.cell.column}) "
            f"changed from {self.previous_value} to {self.new_value} at {self.timestamp}"
        )

# Mark
class Note(models.Model):
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE, related_name = "note")
    value = models.JSONField()

    def __str__(self):
        return f"Notes for Cell ({self.cell.row}, {self.cell.column}) in Session {self.cell.session.id}"
