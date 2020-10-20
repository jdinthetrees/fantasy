from django.db import models
import re

# Create your models here.

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors= {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['name']) < 2:
            errors['name'] = "First name must be at least two characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email does not match"
        if len(postData['email']) < 6:
            errors['email_length'] = "Email should be at least six characters"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least six characters"
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords do not match! try again!"
        return errors

    def login_validator(self, postData):
        errors= {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email does not match"
        if len(postData['email']) < 6:
            errors['email_length'] = "Email should be at least six characters"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least six characters"
        return errors



class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Player(models.Model):
    name = models.CharField(max_length=255)
    pts = models.IntegerField()
    ast = models.IntegerField()
    blk = models.IntegerField()
    reb = models.IntegerField()
    stl = models.IntegerField()
    starter = models.BooleanField(default=False)
    picked = models.BooleanField(default=False)
    # avail = models.BooleanField(default=False)
    # roster = models.ForeignKey(Roster, related_name="players", on_delete = models.CASCADE)
    # draft = models.ForeignKey(Draft, related_name="players", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    

class Roster(models.Model):
    user = models.OneToOneField(User, related_name="roster", on_delete = models.CASCADE)  
    players = models.ManyToManyField(Player, related_name="rosters")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class Lineup(models.Model):
#     rosters = models.ManyToManyField(Roster, related_name="lineups")
    #players = modesl.manytomanyfield(Player, relatedname=lineup)
    
#views.py
# make user
# make a personal roster (their picks)
# # this part wil be in a function after the user selects their starters/lineup
# lineup = current_user.roster.players.filter(started=true).all() # all players for selected user's roster's 
# pts = []
# rbd = []
# for player in lineup:
#     pts.append(player.pts)
#     rbd.append(player.rbd)
# pts_sum = lineup.aggregate(Sum('pts'))
# pts_range = [pts_sum * .85, pts_sum * 1.15]

    
#     Fantasy_Player	(this is a 50 player list)
# Player Name
# Pts
# Ast
# Blk
# Reb
# Stls
# Starter - true/ false prop
# Picked/ not picked
# Available
# Roster- one to many relationship


# Create your models here.
