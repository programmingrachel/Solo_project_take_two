from django.db.models.query import RawQuerySet
from django.shortcuts import redirect, render, HttpResponse
import bcrypt
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import *
from .forms import GoalForm, RegisterForm, LoginForm,TaskForm


def index(request):
    return render(request, 'login.html')


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
                first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
            request.session['user_id'] = user.id
            return redirect('/homepage')
    return redirect('/')


def login(request):
    if request.method == "POST":
        users_with_email = User.objects.filter(email=request.POST['email'])
        if users_with_email:
            user = users_with_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/homepage')
        messages.error(request, 'Email or passord id incorrect')
        return redirect('/')


def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'goals': Goal.objects.all(),
        'tasks': Task.objects.all(),
    }
    form = TaskForm(request.POST)

    return render(request, 'home.html', context, {'form': form})

def setgoal(request):
    context = {
        'goals': Goal.objects.all(),
        'current_user': User.objects.get(id=request.session['user_id']),
        'tasks': Task.objects.all()
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


# def add_task_to_goal(request, task_id):
#     to_update = Task.objects.get(id=task_id)
#     tasks = Task.objects.create(
#     added_to_goal=Goal.objects.get(id=request.session['goal_id']))
#     # created_at=to_update.created_at)
#     # to_delete = Wish.objects.get(id=wish_id)
#     # to_delete.delete()
#     return redirect('/setgoal')

# def task_completed(request, task_id):
#     complete = Task.objects.get(id=task_id)
#     task = Task.objects.create(
#         task =complete.task,
#         goal = complete.added_to_goal,
#         added_by = User.objects.get(id=request.session['user_id']))

#     return redirect('/homepage')


def add_tasks_to_goal(request, goal_id):
    if request.method == "POST":
        errors = {}  # todo take this out
        # errors = Task.objects.task_validator(request.POST)
        # context= {
        # 'current_user': User.objects.get(id=request.session['user_id']),
        #         'goals': Goal.objects.all(),
        #         'tasks': Task.objects.all()
        # }
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/setgoal')
        else:
            user = User.objects.get(id=request.session["user_id"])
            goalinfo = Goal.objects.get(id=goal_id)
            new_task = Task.objects.create(
                task=request.POST['task'],
                goal_setter=user,
                added_to_goal=goalinfo
            )
    context = {
        'goals': Goal.objects.get(id=goal_id),
        'tasks': Task.objects.filter(added_to_goal__id=goal_id)
    }
    return render(request, "adding_tasks.html", context)


def goals(request):
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'goals': Goal.objects.all(),
        'tasks': Task.objects.all()
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
