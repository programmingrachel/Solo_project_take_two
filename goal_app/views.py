from django.db.models.query import RawQuerySet
from django.http import response
from django.shortcuts import redirect, render, HttpResponse
import bcrypt
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import *
import json
import datetime
import requests


def index(request):
    return render(request, 'login.html')

def samplehome(request):
    return render(request, 'samplehome.html')

def samplegoals(request):
    return render(request, 'samplegoals.html')


def create_user(request):
    if request.method == "POST":
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(
                password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name=request.POST['first_name']
                , last_name=request.POST['last_name']
                , email=request.POST['email']
                , password=pw_hash)
            request.session['user_id'] = user.id
            return redirect('/homepage')
    return redirect('/')


def login(request):
    if request.method == "POST":
        if User.objects.filter(email=request.POST['email']).exists():
            users_with_email = User.objects.filter(email=request.POST['email'])
        #if users_with_email:
            user = users_with_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/homepage')
        messages.error(request, 'Email or passord id incorrect')
        return redirect('/')


def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user_id = request.session['user_id']

    if request.method == "POST":
        # use this to update the tasks that are clicked
        tasks = Task.objects.filter(goal_setter__id = user_id, completed_task=False)
        for item in Task.objects.filter(goal_setter__id = user_id, completed_task=False): 
            if request.POST.get("c" + str(item.id)) == "clicked":
                item.completed_task = True
                item.completed_task_date = datetime.date.today()
                item.save()

    if Goal.objects.filter(added_by__id=user_id).exists():
        allgoals = Goal.objects.filter(added_by__id=user_id,completed_goal=False)
    else:
        allgoals = None
    if Task.objects.filter(goal_setter__id = user_id).exists():
        alltasks = Task.objects.filter(goal_setter__id = user_id,completed_task=False)
    else:
        alltasks = None
    context = {
        'current_user': User.objects.get(id=user_id),
        'goals': allgoals,
        'tasks': alltasks,
    }
    return render(request, 'home.html', context)

def setgoal(request):
    quotes = "https://zenquotes.io/api/random"
    response= requests.get(quotes).json()

    context = {
        'goals': Goal.objects.all(),
        'current_user': User.objects.get(id=request.session['user_id']),
        'tasks': Task.objects.all(),
        'quotes': response[0]
    }
    return render(request, "setgoal.html", context)

def create_goal(request):
    if request.method == "POST":
        errors = Goal.objects.goal_validator(request.POST)
        context = {
            'current_user': User.objects.get(id=request.session['user_id']),
        }
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/setgoal')
        else:
            user = User.objects.get(id=request.session["user_id"])
            goals = Goal.objects.create(
                goal=request.POST['goal'],
                desc=request.POST['why'],
                short_term=request.POST['short'],
                start_date=request.POST['starttime'],
                target_date=request.POST['target_date'],
                added_by=User.objects.get(id=request.session['user_id']))
            return redirect('/homepage')

def add_tasks_to_goal(request, goal_id):
    if request.method == "POST":
        errors = {}  # todo take this out
        errors = Task.objects.task_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/{goal_id}/addtasks')
        else:
            user = User.objects.get(id=request.session["user_id"])
            goalinfo = Goal.objects.get(id=goal_id)
            new_task = Task.objects.create(
                task=request.POST['task'],
                goal_setter=user,
                added_to_goal=goalinfo,
                created_at = datetime.date.today()
            )
    context = {
        'goals': Goal.objects.get(id=goal_id),
        'tasks': Task.objects.filter(added_to_goal__id=goal_id),
    'current_user': User.objects.get(id=request.session['user_id']),

    }
    return render(request, "adding_tasks.html", context)


def goals(request):
    quotes = "https://zenquotes.io/api/random"
    response= requests.get(quotes).json()
    user_id = request.session['user_id']
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'active_goals': Goal.objects.filter(added_by__id=user_id, completed_goal=False),
        'completed_goal': Goal.objects.filter(added_by__id=user_id, completed_goal=True).order_by('-completed_goal_date'),
        'active_tasks': Task.objects.filter(goal_setter__id=user_id, completed_task=False).order_by('-created_at'),
        'completed_tasks': Task.objects.filter(goal_setter__id=user_id, completed_task=True).order_by('-completed_task_date'),
        'quotes': response[0]
    }
    return render(request, "view.html", context)


def editgoal(request, goal_id):
    this_goal = Goal.objects.get(id=goal_id)
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'goal': this_goal
    }
    return render(request, "edit.html", context)


def updategoal(request, goal_id):
    errors = Goal.objects.goal_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/{goal_id}/editgoal')
    to_update = Goal.objects.get(id=goal_id)
    to_update.goal = request.POST['goal']
    to_update.desc = request.POST['why']
    to_update.short_term = request.POST['short']
    to_update.start_date = request.POST['starttime']
    to_update.target_date = request.POST['target_date']
    to_update.save()
    return redirect('/homepage')


def delete(request, goal_id):
    to_delete = Goal.objects.get(id=goal_id)
    to_delete.delete()
    return redirect('/homepage')

def goal_completed(request, goal_id):
    tasks = Task.objects.filter(added_to_goal__id = goal_id, completed_task=False)
    for item in tasks: 
        item.completed_task = True
        item.completed_task_date = datetime.date.today()
        item.save()

    to_update = Goal.objects.get(id=goal_id)
    to_update.completed_goal = True
    to_update.completed_goal_date = datetime.date.today()
    to_update.save()
    return redirect('/homepage')


def updateprofile(request, user_id):
    if request.method == "POST":
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/{user_id}/updateprofile')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(
                password.encode(), bcrypt.gensalt()).decode()
            to_update = User.objects.get(id=user_id)
            to_update.first_name = request.POST['first_name']
            to_update.last_name = request.POST['last_name']
            to_update.email = request.POST['email']
            to_update.password = request.POST['password']
            to_update.confirm = request.POST['confirm']
            to_update.save()
    return redirect('/homepage')


def editprofile(request):
    return render(request, "profile.html")


def logout(request):
    request.session.flush()
    return redirect('/')
