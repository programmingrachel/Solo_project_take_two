from django.urls import path
from . import views

urlpatterns = [
path('', views.index),
path('user/create',views.create_user),
path('users/login',views.login),
path('homepage',views.home),
path('setgoal',views.setgoal),
path('create_goal',views.create_goal),
path('create_task',views.create_task),
path('<int:goal_id>/editgoal',views.editgoal),
path('<int:goal_id>/update',views.updategoal),
path('<int:goal_id>/delete',views.delete),
path('viewgoals',views.goals),
path('editprofile',views.editprofile),
path('logout',views.logout)

]