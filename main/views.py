from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Player, Roster
import bcrypt
import random

def index(request):

    if 'user_id' in request.session:
        return redirect('/dashboard')
    context = {
        'all_users': User.objects.all(),
    }

    return render(request, "index.html")

def register(request):
    return render(request, 'registration.html')

def login_user(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for msg in errors.values():
            messages.error(request, msg)
        return redirect('/')
    email_users = User.objects.filter(email=request.POST['email'])
    
    our_user = email_users[0]
    if bcrypt.checkpw(request.POST['password'].encode(), our_user.password.encode()):
        request.session['user_id'] = our_user.id
        return redirect('/dashboard')
    messages.error(request, "password does not match try again!")
    return redirect('/')


def process_user(request):

    if 'user_id' in request.session:
        return redirect('/dashboard')
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for msg in errors.values():
            messages.error(request, msg)
        return redirect('/')

    password = request.POST['password']
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    # print(password, "\n", hashed )
    user = User.objects.create(
        name=request.POST['name'],
        email=request.POST['email'],
        password=hashed,
    )
    
    Roster.objects.create(user=user)
    
    
    request.session['user_id'] = user.id
    return redirect('/dashboard')

def welcome(request):
    if 'user_id' not in request.session:
        return redirect('/')
    
    context = {
        'current_user': User.objects.get(id=request.session['user_id'])
    }

    return render(request, "dashboard.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')

def roster_add(request, player_id):
    user = User.objects.get(id=request.session['user_id'])
    player = Player.objects.get(id=player_id)
    this_roster = user.roster
    if len(this_roster.players.all())<10:
        this_roster.players.add(player)
        player.picked = True  
        player.save()
    
    
    print(user.roster.players.all())
    print(player.name, player.picked)
    return redirect('/draft')

# Create your views here.

def draft_view(request):
    user = User.objects.get(id=request.session['user_id'])
    request.session['lineup'] = ''
    
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'players': Player.objects.all(),
        'roster': user.roster
    }
    
    
    return render(request, 'draft.html', context)

def lineup_view(request):
    user = User.objects.get(id=request.session['user_id'])
    
    context = {
        'current_user': user,
        'roster': user.roster
    }
    
    return render(request, 'lineup.html', context)

def lineup_process(request, player_id):
    id_array = request.session['lineup'].split('|')
    if len(id_array)<=3:
        user = User.objects.get(id=request.session['user_id'])
        player = Player.objects.get(id=player_id)
        request.session['lineup'] += (str(player_id)+'|')
    
    print(request.session['lineup'])
    
    return redirect('/lineup')

def gameplay(request):
    player = Player.objects.get(id=request.POST['player_id'])
    points = (player.pts+player.stl+(player.ast//2)+(player.blk//2)+(player.reb//2))
    random_points= random.randint(points - 5, points + 5)
    request.session['points'] = random_points
    print(random_points)
    
    return redirect('/lineup')