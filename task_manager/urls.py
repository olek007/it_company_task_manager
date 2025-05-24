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
    PositionCreateView,
    TeamCreateView,
    WorkerCreateView,
    ProjectCreateView,
)

urlpatterns = [
    path("", index, name="index"),
    path("task_types/", TaskTypeListView.as_view(), name="task_type-list"),
    path("task_types/<int:pk>", TaskTypeDetailView.as_view(), name="task_type-detail"),
    path("task_types/create", TaskTypeCreateView.as_view(), name="task_type-create"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/<int:pk>", PositionDetailView.as_view(), name="position-detail"),
    path("positions/create", PositionCreateView.as_view(), name="position-create"),
    path("teams/", TeamListView.as_view(), name="team-list"),
    path("teams/<int:pk>", TeamDetailView.as_view(), name="team-detail"),
    path("teams/create", TeamCreateView.as_view(), name="team-create"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create", WorkerCreateView.as_view(), name="worker-create"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("projects/<int:pk>", ProjectDetailView.as_view(), name="project-detail"),
    path("projects/create", ProjectCreateView.as_view(), name="project-create"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>", TaskDetailView.as_view(), name="task-detail"),
]
app_name = "task_manager"
