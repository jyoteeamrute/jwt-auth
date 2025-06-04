
from django.urls import path
from .views import *

urlpatterns = [
    path("register/",UserRegistrationView.as_view()),
    path("login/",LoginView.as_view()),
    path("user/",UserDetailView.as_view()),

    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]

