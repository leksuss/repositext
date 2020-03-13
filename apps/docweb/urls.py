from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf.urls import url
from .views import IndexView, RepositoryView, UserHomeView, AddDocumentView, PAGE_TITLE
from django.contrib.auth import views as auth_views


urlpatterns = [
    path(
        '', login_required(IndexView.as_view()), name="index-view"
    ),
    path(
        'home/<str:username>/', login_required(UserHomeView.as_view()),
        name="user-home-view"
    ),
    path(
        'repository/folder/<uuid:folder_id>/',
        login_required(RepositoryView.as_view()),
        name="repo-view"
    ),
    path(
        'repository/folder/<uuid:folder_id>/document/add/', 
        login_required(AddDocumentView.as_view()),
        name="add-document-view"
    ),
    path(
        'login/',
        auth_views.LoginView.as_view(
            extra_context={
                'page_title': PAGE_TITLE,
            }
        ),
        name='login'
        
    ),
    path(
        'logout/', auth_views.LogoutView.as_view(),
        {'next_page': '/login'}, name='logout'
    ),
]
