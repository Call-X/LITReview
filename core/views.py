from django.contrib.auth import login, authenticate
from .forms import LoginForm, UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView, CreateView
from django.views.generic import View
from django.urls import reverse_lazy
from core import forms


class HomeView(FormView):

    template_name = "core/base.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")


class RegistrationView(CreateView):
    template_name = "core/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("home")


class LoginView(View):
    form_class = forms.LoginForm
    template_name = "core/signin.html"

    def get(self, request):
        form = self.form_class()
        message = ""
        return render(
            request, self.template_name, context={"form": form, "message": message}
        )

    def post(self, request):
        if request.methode == "POST":
            form = forms.LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(
                    username=form.cleaned_data["username"],
                    passeword=form.cleaned_data["passeword"],
                )
                if user is not None:
                    login(request, user)
                    return redirect("home")
            message = "Identification invalid."
            return render(
                request, self.template_name, context={"form": form, "message": message}
            )


class LogoutView(View):
    template_name = "core/base.html"


def error_404(request, exception):
    return render(request, "core/404.html")
