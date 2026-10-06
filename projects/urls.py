from django.urls import path

from projects.views import ProjectListView, ProjectDetailView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView

app_name = 'projects'

urlpatterns = [
    path("", ProjectListView.as_view(), name="project_list"),
    path("<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("create/", ProjectCreateView.as_view(), name="project_create"),
    path("<int:pk>/update/", ProjectUpdateView.as_view(), name="project_update"),
    path("<int:pk>/delete/", ProjectDeleteView.as_view(), name="project_delete"),
]