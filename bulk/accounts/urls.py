from django.urls import path
from .views import SignUpView
from . import views

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('settings/', views.settings, name='settings'),
    path('login_redirect', views.login_redirect, name='login_redirect'),
]