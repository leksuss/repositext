from django.urls import path
from .views import IndexView, RepositoryView


urlpatterns = [
    path('', IndexView.as_view(), name="index-view"),
    path('repository/folder/-ROOT-/', RepositoryView.as_view(), name="repository-view"),
    path('repository/folder/<uuid:folder_id>/', RepositoryView.as_view(), name="repo-view"),
]
