from django.urls import path

from tasks.views import TaskListView
from workers.views import WorkerListView, WorkerDetailView, WorkerCreateView, WorkerUpdateView, WorkerDeleteView

app_name = "workers"

urlpatterns = [
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),
]