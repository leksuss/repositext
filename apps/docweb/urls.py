from django.urls import path
from .views import IndexView, RepositoryView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', IndexView.as_view(), name="index-view"),
    path('repository/folder/-ROOT-/', RepositoryView.as_view(), name="repository-view"),
    path('repository/folder/<uuid:folder_id>/', RepositoryView.as_view(), name="repo-view"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': '/login'}, name='logout'),
]
