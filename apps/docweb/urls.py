from django.urls import path
from .views import IndexView, RepositoryView


urlpatterns = [
    path('', IndexView.as_view(), name='home-page'),
    path('repository/folder/-ROOT-/', RepositoryView.as_view()),
    path('repository/folder/<uuid:folder_id>/', RepositoryView.as_view()),
]
