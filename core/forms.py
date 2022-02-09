from dataclasses import fields
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model


class LogForm(forms.Form):
    log = forms.CharField()

class UserCreationForm(auth_forms.UserCreationForm):

    class Meta(auth_forms.UserCreationForm.Meta):
        model = get_user_model()
        fields = ["username", 'first_name', 'email']

class LoginForm(forms.Form):
    log = forms.CharField
