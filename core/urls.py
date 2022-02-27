
from django.urls import path
from core.views import HomeView
from core.views import RegistrationView
from django.contrib.auth.views import LoginView, LogoutView



urlpatterns = [
    path('', HomeView.as_view(template_name='core/base.html'), name="home"),
    path('signin/', LoginView.as_view(template_name='core/signin.html'), name="signin"),
    path('register/', RegistrationView.as_view(template_name= "core/register.html"), name="users_register"), 
    path('signout/', LogoutView.as_view(template_name='core/base.html'), name="signout"),

]




