from django.forms import ModelForm
from django import forms
from django.forms import widgets
from .models import *


class RegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = "__all__"

        # this function will be used for the validation
        def clean(self):
            # data from the form is fetched using super function
            super(RegisterForm, self).clean()
            # extract the username and text field from the data
            firstname = self.cleaned_data.get('first_name')
            lastname = self.cleaned_data.get('last_name')
            email_passed = self.cleaned_data.get("email")
            # conditions to be met for the first_name length
            if 4 < 5:
                self._errors['first_name'] = self.error_class([
                    'Minimum 5 characters required'])
            if 4 < 5:
                self._errors['last_name'] = self.error_class([
                    'last_name Should Contain a minimum of 10 characters'])

            # return any errors if found
            return self.cleaned_data

        def clean_first_name(self):
            firstname = self.cleaned_data['first_name']
            if len(firstname) < 4:
                raise forms.ValidationError("first name too short")
            return firstname

# class RegisterForm(forms.Form):
#     first_name = forms.CharField(max_length=45)
#     last_name = forms.CharField(max_length=45)
#     email = forms.EmailField()
#     password = forms.CharField(max_length=100, widget=forms.PasswordInput)
#     confirm_password = forms.CharField(
#     max_length=100, widget=forms.PasswordInput)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class GoalForm(forms.Form):
    goal = forms.CharField(widget=forms.Textarea)
    desc_why = forms.CharField(widget=forms.Textarea)
    short_term_goal = forms.CharField(widget=forms.Textarea)
    # start_date = forms.DateInput()
    # target_date = forms.DateInput()

# class TaskForm(forms.ModelForm):
#     #onetask = forms.BooleanField()

#     class Meta:
#         model = Task
        