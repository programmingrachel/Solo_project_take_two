from django.shortcuts import redirect, render, HttpResponse
import bcrypt
from django.contrib import messages
from .models import *


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
        'goals': Goal.objects.all()
        # 'added_wishes': Wish_added.objects.filter(added_by__id=request.session['user_id'])
    }
    return render(request, 'home.html', context)

        # return render(request, "home.html")

def setgoal(request):
    context= {
        'current_user': User.objects.get(id=request.session['user_id']),
    }
    return render(request,"setgoal.html",context)

def create_goal(request):
    if request.method == "POST":
        errors = Goal.objects.goal_validator(request.POST)
        context= {
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

def create_task(request):
    if request.method == "POST":
        errors = Task.objects.task_validator(request.POST)
        context= {
        'current_user': User.objects.get(id=request.session['user_id']),
                'goals': Goal.objects.all()
        }
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/setgoal')
        else:
            user = User.objects.get(id=request.session["user_id"])
            task = Task.objects.create(
                task=request.POST['task'],
                added_to_goal=Goal.objects.get(id=request.session['user_id'])
                )
            return redirect('/homepage', context)
def goals(request):
    context= {
        'current_user': User.objects.get(id=request.session['user_id']),
                'goals': Goal.objects.all(),
                'tasks': Task.objects.all()
        }
    return render(request,"view.html",context )


def editgoal(request,goal_id):
    this_goal = Goal.objects.get(id=goal_id)
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'goal': this_goal
    }
    return render(request,"edit.html",context )

def updategoal(request, goal_id):
    errors = Goal.objects.goal_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/{goal_id}/editgoal')
    to_update = Goal.objects.get(id=goal_id)
    to_update.goal = request.POST['goal']
    to_update.desc = request.POST['why']
    to_update.short_term=request.POST['short']
    to_update.start_date=request.POST['starttime']
    to_update.target_date=request.POST['target_date']
    to_update.save()
    return redirect('/homepage')

def delete(request, goal_id):
    to_delete = Goal.objects.get(id=goal_id)
    to_delete.delete()
    return redirect('/homepage')



def editprofile(request):
    return render (request, "profile.html")

def logout(request):
    request.session.flush()
    return redirect('/')
