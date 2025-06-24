from django.urls import path
from . import views

urlpatterns = [
    path('get_session/', views.get_session),
    path('start_game/', views.start_game),
    path('save_game_state/', views.save_game_state),
    path('get_game_state/', views.get_game_state),
    path('', views.index, name='home'),  # This is the root URL
    path('get_puzzle/', views.get_current_puzzle, name="get_puzzle"),
    path('new_game/', views.new_game, name="new_game"),
    path('is_correct/', views.is_correct, name="is_correct"),
    path('new_session/', views.new_session, name="new_session"),
    path('update_cell/', views.update_cell, name="update_cell"),
    path('reset_cell/', views.reset_cell, name="reset_cell"),
    path('set_note/', views.set_note, name="set_note"),
    path('get_notes/', views.get_notes, name="get_notes"),
    path('clear_notes/', views.clear_notes, name="clear_notes"),
    path('get_history/', views.get_history, name="get_history"),
    path('update_history/', views.update_history, name="update_history"),
    path('undo/', views.undo, name="undo"),
    path('undo_till_correct/', views.undo_till_correct, name="undo_till_correct"),
]
