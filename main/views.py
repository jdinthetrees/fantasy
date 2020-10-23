from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Player, Roster
import bcrypt
import random

# computer = User(name='PC2')
# computer_roster = Roster(id=99, user=computer)


    

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
        user = User.objects.get(id=request.session['user_id'])
        
        # Roster.objects.create(user=user)
        print(user.roster)
        
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

def comp_draft_play(request):
    avail_players = []
    for player in Player.objects.all():
        if player.picked == False:
            avail_players.append(player)
            
    comp_pick_index = random.randint(0, len(avail_players)-1)
    player = avail_players[comp_pick_index]
    print(player.name)
    
    computer = User.objects.get(id=99)
    
    computer.roster.players.add(player)
    player.picked = True  
    player.save()
    
    print('all players: ', computer.roster.players.all())
    
    
    print('comp_pick_index: ', comp_pick_index)
    return redirect('/draft')
    
    

def roster_add(request, player_id):
    user = User.objects.get(id=request.session['user_id'])
    player = Player.objects.get(id=player_id)
    this_roster = user.roster
    if len(this_roster.players.all())<9:
        this_roster.players.add(player)
        player.picked = True  
        player.save()
        return redirect('/comp_draft_play')
    
    
    
    print(user.roster.players.all())
    print(player.name, player.picked)
    return redirect('/draft')

# Create your views here.


def draft_view(request):
    user = User.objects.get(id=request.session['user_id'])
    request.session['winning_scores'] = ''
    request.session['comp_winning_scores'] = ''
    request.session['game_count'] = 0
    avail_players = []
    for player in Player.objects.all():
        if player.picked == False:
            avail_players.append(player)
            
    roster_length = len(user.roster.players.all())
    computer = User.objects.get(id=99)
    comp_roster = computer.roster.players.all()
    
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        # 'players': Player.objects.all(),
        'players': avail_players,
        'roster': user.roster,
        'roster_length': roster_length,
        'comp_roster': comp_roster
    }
    
    return render(request, 'draft.html', context)

def lineup_view(request):
    winner = ''
    user = User.objects.get(id=request.session['user_id'])
    winning_scores_array = request.session['winning_scores'].split('|')
    winning_scores_array.pop()
    
    comp_winning_scores_array = request.session['comp_winning_scores'].split('|')
    comp_winning_scores_array.pop()
    
    print('winning_scores_array: ', winning_scores_array)
    print('comp_winning_scores_array: ', comp_winning_scores_array)
    
    if len(comp_winning_scores_array)>4:
        comp_wins_total = 0
        user_wins_total = 0
        for i in range(0, len(winning_scores_array)):  
            if int(winning_scores_array[i]) > int(comp_winning_scores_array[i]):
                user_wins_total += 1
            else:
                comp_wins_total += 1
        if user_wins_total > comp_wins_total:
            winner = 'user'
        else:
            winner = 'comp'
        
    print('winner', winner)
    
    context = {
        'current_user': user,
        'roster': user.roster,
        'winning_scores_array': winning_scores_array,
        'comp_winning_scores_array': comp_winning_scores_array,
        'winner': winner,
        # 'all_winning_scores_array': all_winning_scores_array
    }
    
    return render(request, 'lineup.html', context)



def gameplay(request):
    request.session['game_count'] += 1
    print('game_count', request.session['game_count'])
    
    print(request.POST)
    computer = User.objects.get(id=99)
    comp_roster = computer.roster.players.all()
    # print('test: ', comp_roster[6:9])
    comp_pick_index = random.randint(0, 6)
    comp_picks = comp_roster[comp_pick_index:(comp_pick_index+3)]
    comp_picks_ids = []
    for pick in comp_picks:
        comp_picks_ids.append(pick.id)
        
    for i in range(0,3,1):
        # print(i, id_array[i])
        
        if i == 0:
            comp_player1 = Player.objects.get(id=int(comp_picks_ids[0]))
            comp_starter1 = comp_player1.name
            comp_points1 = (comp_player1.pts+comp_player1.stl+(comp_player1.ast//2)+(comp_player1.blk//2)+(comp_player1.reb//2))
            comp_random_points1= random.randint(comp_points1 - 5, comp_points1 + 5)
            request.session['comp_points1'] = comp_random_points1
            request.session['comp_starter1'] = comp_starter1
            print('comp: ', comp_random_points1)
        elif i == 1:
            comp_player2 = Player.objects.get(id=int(comp_picks_ids[1]))
            comp_starter2 = comp_player2.name
            comp_points2 = (comp_player2.pts+comp_player2.stl+(comp_player2.ast//2)+(comp_player2.blk//2)+(comp_player2.reb//2))
            comp_random_points2 = random.randint(comp_points2 - 5, comp_points2 + 5)
            request.session['comp_points2'] = comp_random_points2
            request.session['comp_starter2'] = comp_starter2
            print('comp: ', comp_random_points2)
        else:
            comp_player3 = Player.objects.get(id=int(comp_picks_ids[2]))
            comp_starter3 = comp_player3.name
            comp_points3 = (comp_player3.pts+comp_player3.stl+(comp_player3.ast//2)+(comp_player3.blk//2)+(comp_player3.reb//2))
            comp_random_points3= random.randint(comp_points3 - 5, comp_points3 + 5)
            request.session['comp_points3'] = comp_random_points3
            request.session['comp_starter3'] = comp_starter3
            print('comp: ', comp_random_points3)
    
    comp_total_points = comp_random_points1+comp_random_points2+comp_random_points3
    print('comp: ', comp_total_points)
    request.session['comp_total_points'] = comp_total_points
    
    request.session['comp_winning_scores'] += str(comp_total_points)+'|'
    print(request.session['comp_winning_scores'])
    

    id_array = request.POST.getlist('player_id')
    # print(id_array)

    for i in range(0,3,1):
        # print(i, id_array[i])
        
        if i == 0:
            player1 = Player.objects.get(id=int(id_array[0]))
            starter1 = player1.name
            points1 = (player1.pts+player1.stl+(player1.ast//2)+(player1.blk//2)+(player1.reb//2))
            random_points1= random.randint(points1 - 5, points1 + 5)
            request.session['points1'] = random_points1
            request.session['starter1'] = starter1
            print(random_points1)
        elif i == 1:
            player2 = Player.objects.get(id=int(id_array[1]))
            starter2 = player2.name
            points2 = (player2.pts+player2.stl+(player2.ast//2)+(player2.blk//2)+(player2.reb//2))
            random_points2 = random.randint(points2 - 5, points2 + 5)
            request.session['points2'] = random_points2
            request.session['starter2'] = starter2
            print(random_points2)
        else:
            player3 = Player.objects.get(id=int(id_array[2]))
            starter3 = player3.name
            points3 = (player3.pts+player3.stl+(player3.ast//2)+(player3.blk//2)+(player3.reb//2))
            random_points3= random.randint(points3 - 5, points3 + 5)
            request.session['points3'] = random_points3
            request.session['starter3'] = starter3
            print(random_points3)
        
    total_points = random_points1+random_points2+random_points3
    print(total_points)
    request.session['total_points'] = total_points
    
    request.session['winning_scores'] += str(total_points)+'|'
    print(request.session['winning_scores'])

    return redirect('/lineup')



def delete_roster(request, roster_id):
    print('roster_id: ', roster_id)
    
    for player in Player.objects.all():
        player.picked = False
        player.save()
    
    this_roster = Roster.objects.get(id=roster_id)
    this_roster.delete()
    user = User.objects.get(id=request.session['user_id'])
    Roster.objects.create(user=user)
    
    computer = User.objects.get(id=99)
    comp_roster = computer.roster.players.all()
    for player in comp_roster:
        computer.roster.players.remove(player)
    
    return redirect('/dashboard')

def new_game(request, roster_id):
    print('roster_id: ', roster_id)
    
    for player in Player.objects.all():
        player.picked = False
        player.save()
    
    this_roster = Roster.objects.get(id=roster_id)
    this_roster.delete()
    user = User.objects.get(id=request.session['user_id'])
    Roster.objects.create(user=user)
    
    computer = User.objects.get(id=99)
    comp_roster = computer.roster.players.all()
    for player in comp_roster:
        computer.roster.players.remove(player)
    
    return redirect('/draft')