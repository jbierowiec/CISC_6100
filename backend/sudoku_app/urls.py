from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # This is the root URL
    path('get_puzzle/', views.get_current_puzzle, name="get_puzzle"),
    path('check_solution/', views.check_solution, name="check_solution"),
    path('is_correct/', views.is_correct, name="is_correct"),
    path('new_game/', views.new_game, name="new_game"),
    path('new_session/', views.new_session, name="new_session"),
    path('update_cell/', views.update_cell, name="update_cell"),
    path('get_history/', views.get_history, name="get_history"),
]
