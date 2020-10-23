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
    path('game_play', views.gameplay),
    path('delete_roster/<roster_id>', views.delete_roster),
    path('comp_draft_play', views.comp_draft_play),
    path('new_game/<roster_id>', views.new_game),

]