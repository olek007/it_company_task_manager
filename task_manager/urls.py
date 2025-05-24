from django.urls import path

from task_manager.views import (
    index,
    TaskTypeListView,
    PositionListView,
    TeamListView,
    WorkerListView,
    ProjectListView,
    TaskListView,
    TaskTypeDetailView,
    PositionDetailView,
    TaskDetailView,
    ProjectDetailView,
    WorkerDetailView,
    TeamDetailView,
    TaskTypeCreateView,
)

urlpatterns = [
    path("", index, name="index"),
    path("task_types/", TaskTypeListView.as_view(), name="task_type-list"),
    path("task_types/<int:pk>", TaskTypeDetailView.as_view(), name="task_type-detail"),
    path("task_types/create", TaskTypeCreateView.as_view(), name="task_type-create"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/<int:pk>", PositionDetailView.as_view(), name="position-detail"),
    path("teams/", TeamListView.as_view(), name="team-list"),
    path("teams/<int:pk>", TeamDetailView.as_view(), name="team-detail"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>", WorkerDetailView.as_view(), name="worker-detail"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("projects/<int:pk>", ProjectDetailView.as_view(), name="project-detail"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>", TaskDetailView.as_view(), name="task-detail"),
]
app_name = "task_manager"
