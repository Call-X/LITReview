
from django.urls import path
from core.views import HomeView
from core.views import RegistrationView
from django.contrib.auth.views import LoginView



urlpatterns = [
    path('', HomeView.as_view(), name ="home"),
    path('signin/', LoginView.as_view(), name="signin"),
    path('register/', RegistrationView.as_view(), name="users_register"), 
]


