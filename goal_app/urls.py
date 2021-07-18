from django.urls import path
from . import views

urlpatterns = [
path('', views.index, name="index"),
path('samplehome',views.samplehome),
path('samplegoals',views.samplegoals),
path('user/create',views.create_user),  #don't need this
path('users/login',views.login),    #this should be a separate page
path('homepage',views.home),
path('setgoal',views.setgoal),
path('create_goal',views.create_goal),
path('<int:goal_id>/addtasks',views.add_tasks_to_goal),

# path('<int:task_id>/add_task_to_goal',views.add_task_to_goal),
path('<int:goal_id>/editgoal',views.editgoal),
path('<int:goal_id>/update',views.updategoal),
path('<int:goal_id>/delete',views.delete),
path('<int:user_id>/updateprofile',views.updateprofile),
path('viewgoals',views.goals),
path('editprofile',views.editprofile),
# path('<int:task_id>/completed',views.task_completed),


path('addtasks',views.add_tasks_to_goal),
path('logout',views.logout)
]