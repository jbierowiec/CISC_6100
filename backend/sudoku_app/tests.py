from django.test import TestCase, Client
from django.urls import reverse, resolve
from .models import Sessions, SudokuGames, Cell
from .views import new_game, is_correct 

# Create your tests here.
class SudokuGamesModelTest(TestCase):
    def setUp(self):
        self.game = SudokuGames.objects.create(
            puzzle=[[0, 1], [1, 0]],
            solution=[[1, 0], [0, 1]],
            difficulty='easy',
            size=2
        )
    
    def test_game_creation(self):
        self.assertEqual(SudokuGames.objects.count(), 1)
        self.assertEqual(self.game.difficulty, 'easy')
        self.assertEqual(self.game.size, 2)

class CellModelTest(TestCase):
    def setUp(self):
        self.game = SudokuGames.objects.create(
            puzzle=[[0, 1], [1, 0]],
            solution=[[1, 0], [0, 1]],
            difficulty='easy',
            size=2
        )
        self.session = Sessions.objects.create(sudoku_game=self.game)
        self.cell = Cell.objects.create(
            session=self.session, row=0, column=0, value=0, solution=1, pre_filled=False
        )
    
    def test_cell_creation(self):
        self.assertEqual(Cell.objects.count(), 1)
        self.assertEqual(self.cell.solution, 1)
        self.assertFalse(self.cell.pre_filled)

class SudokuViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.game = SudokuGames.objects.create(
            puzzle=[[0, 1], [1, 0]],
            solution=[[1, 0], [0, 1]],
            difficulty='easy',
            size=2
        )
        self.session = Sessions.objects.create(sudoku_game=self.game)
    
    def test_new_game_view(self):
        response = self.client.get('/new_game/', {'difficulty': 'easy', 'size': 2})
        self.assertEqual(response.status_code, 404)

    def test_is_correct_view(self):
        response = self.client.post('/is_correct/', {
            'row': 0, 'col': 0, 'session_id': self.session.id, 'userValue': 1
        }, content_type='application/json')
        self.assertEqual(response.status_code, 404)

class URLTests(TestCase):
    def test_new_game_url(self):
        url = reverse('new_game')
        self.assertEqual(resolve(url).func, new_game)

    def test_is_correct_url(self):
        url = reverse('is_correct')
        self.assertEqual(resolve(url).func, is_correct)