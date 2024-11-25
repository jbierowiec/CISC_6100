from django.db import models

# Create your models here.

class SudokuGames(models.Model):
    puzzle = models.JSONField()
    solution = models.JSONField()
    difficulty = models.CharField(max_length=50)
    size = models.IntegerField()

    def __str__(self):
        return f"{self.difficulty} {self.size}x{self.size} Sudoku"
    
