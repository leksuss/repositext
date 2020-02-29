from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView


urlpatterns = [
    path('signup/', views.SignUp.as_view()),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.Home.as_view(), name='home'),
]