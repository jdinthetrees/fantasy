from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login_user', views.login_user),
    path('process_user', views.process_user),
    path('dashboard', views.welcome),
    path('logout', views.logout),
    path('draft', views.draft_view),
    path('roster_add/<player_id>', views.roster_add),
    path('lineup', views.lineup_view),
    path('lineup_process/<player_id>', views.lineup_process),
    path('game_play', views.gameplay)

]