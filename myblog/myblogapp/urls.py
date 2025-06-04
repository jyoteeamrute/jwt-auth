
from django.urls import path
from .views import *

urlpatterns = [
    path("register/",UserRegistrationView.as_view()),
    path("login/",LoginView.as_view()),
    path("user/",UserDetailView.as_view())
]