from os import error
from django.db import models
import re
from django.db.models.fields import DateField
import datetime
from django.forms.widgets import CheckboxSelectMultiple
import bcrypt
from django.core import validators
from django.core.exceptions import ValidationError

def firstCapitalLetter(value):
    if value != value.title():
        raise ValidationError(f"{value}'s first letter needs a capital (like {value.title()})")

def validateLengthGreaterThanTwo(value):
    if len(value) < 3:
        raise ValidationError(
            '{} must be longer than: 2'.format(value)
        )
def emailvalidator(value):
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'),
    # users_with_email = User.objects.filter(email=reqPOST['email'])

    if not EMAIL_REGEX(value):    # test whether a field matches the pattern
        if len(value) >= 1:
            raise ValidationError('{} Invalid email address!'.format(value),'{} Email already in use'.format(value))




class UserManager(models.Manager):
    def user_validator(self, reqPOST):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(reqPOST['first_name']) < 3:
            errors["first_name"] = "First Name must have a minimum of 3 characters"
        if len(reqPOST['last_name']) < 3:
            errors["last_name"] = "Last Name must have a minimum of 3 characters"
        if len(reqPOST['email']) < 5:
            errors["email"] = "Email is to short"
        if len(reqPOST['password']) < 6:
            errors["password"] = "Password is to short"
        if reqPOST['password'] != reqPOST['confirm']:
            errors['match'] = "Passwords don't match"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqPOST['email']):    # test whether a field matches the pattern            
            errors['regex'] = "Invalid email address!"
        users_with_email = User.objects.filter(email=reqPOST['email'])
        if len(users_with_email) >= 1:
            errors['dup'] = "Email already in use"
        return errors
    def update_validator(self, POSTdata):
        errors = {}
        if len(POSTdata['first_name']) < 3:
            errors["first_name"] = "First Name must have a minimum of 3 characters"
        if len(POSTdata['last_name']) < 3:
            errors["last_name"] = "Last Name must have a minimum of 3 characters"
        if len(POSTdata['email']) < 5:
            errors["email"] = "Email is to short"
        if len(POSTdata['password']) < 6:
            errors["password"] = "Password is to short"
        if POSTdata['password'] != POSTdata['confirm']:
            errors['match'] = "Passwords don't match"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(POSTdata['email']):    # test whether a field matches the pattern            
            errors['regex'] = "Invalid email address!"
        return errors


class User(models.Model):
    # first_name = models.CharField(max_length=255,validators=[validators.MinLengthValidator(5,"First name too short"),firstCapitalLetter,])
    # last_name = models.CharField(max_length=255, validators= [validators.MinLengthValidator(5,"Last name too short"),])
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=25)
    confirm = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return ' {} {}'.format(self.first_name, self.last_name)

    # def clean(self):
    #     if self.password != self.confirm:
    #         raise ValidationError({'password': _('Your passwords don''t match')})

class GoalManager(models.Manager):
    def goal_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['goal']) <3:
            errors['goal'] = "goal must have a minimum of 3 characters"
        if len(reqPOST['why']) <3:
            errors['why'] = "Please explain more about why?"
        # validate dates given
        today = datetime.datetime.now()
        start_date = datetime.datetime.strptime(reqPOST['starttime'], "%m/%d/%Y")
        target_date = datetime.datetime.strptime(reqPOST['target_date'], "%m/%d/%Y")
        if start_date < today:
            errors['starttime'] = "Your goal can't start in the past"
        if start_date > target_date:
            errors['target_date'] = "Your target date is before the goal start"
        return errors 


class Goal(models.Model):
    goal = models.CharField(max_length=255)
    desc= models.CharField(max_length=255)
    short_term= models.CharField(max_length=255)
    start_date=models.DateField(auto_now=False,default='null')
    target_date=models.DateField(auto_now=False, default='null')
    tasks = models.ManyToManyField(User, related_name="tasks_for_goal")
    added_by = models.ForeignKey(User, related_name="users_goal",on_delete=models.CASCADE,null= True)
    completed_goal= models.BooleanField(default=False, null=True )
    completed_goal_date=models.DateField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= GoalManager()
    def __str__(self):
        return ' {} {}'.format(self.goal, self.goal,self.tasks)

class TaskManager(models.Manager):
    def task_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['task']) <=0:
            errors['task'] = "Please enter task"
        return errors
    
class Task(models.Model):
    task=models.CharField(max_length=100)
    goal_setter=models.ForeignKey(User, related_name="made_goal", on_delete=models.CASCADE,null= True)
    added_to_goal = models.ForeignKey(Goal, related_name="task_for_goal", on_delete=models.CASCADE,null= True)
    completed_task= models.BooleanField(default=False, null=True )
    completed_task_date=DateField(default=None,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=TaskManager()
    
    def __str__(self):
        return ' {} {}'.format(self.task, self.goal_setter,self.added_to_goal)

