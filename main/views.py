from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Player, Roster
import bcrypt

def index(request):

    if 'user_id' in request.session:
        return redirect('/dashboard')
    context = {
        'all_users': User.objects.all(),
    }

    return render(request, "index.html")

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
        f_name=request.POST['f_name'],
        l_name=request.POST['l_name'],
        email=request.POST['email'],
        password=hashed,
    )
    request.session['user_id'] = user.id
    return redirect('/dashboard')

def welcome(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
    }

    return render(request, "dashboard.html", context)







def logout(request):
    request.session.clear()
    return redirect('/')

# Create your views here.
