from email import message
from turtle import home
from django.contrib.auth import login, authenticate, logout
from re import template
from sre_constants import SUCCESS

from . import forms
from .forms import LogForm, UserCreationForm
from django.shortcuts import redirect, render
from datetime import datetime
from django.views.generic.edit import FormView, CreateView
from django.views.generic import View


from django.urls import reverse_lazy

from core import forms


class HomeView(FormView):
    

    template_name = "core/index.html"
    form_class = LogForm
    success_url = reverse_lazy("core : home")

class RegistrationView(CreateView):
    template_name = "core/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("core : home")

class loginPage(View):
    form_class = forms.LoginForm
    template_name = 'core/signin.html'

    def get(self, request):
        form = self.form_class()
        message = ''
        return render( request, self.template_name, context={'form' : form, 'message' : message})

    def post(self, request):
        if request.methode == 'POST':
            form = forms.LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(
                    username=form.cleaned_data['username'],
                    passeword=form.cleaned_data['passeword'],
                )
                if user is not None:
                    login(request, user)
                    return redirect('home')
            message = 'Identification invalid.'
            return render(request, self.template_name, context={'form' : form, 'message' : message})
