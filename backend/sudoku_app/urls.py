from django.urls import path
from . import views

urlpatterns = [
    path('get_puzzle/', views.get_current_puzzle, name="get_puzzle"),
    path('check_solution/', views.check_solution, name="check_solution"),
    path('new_game/', views.new_game, name="new_game"),
]
