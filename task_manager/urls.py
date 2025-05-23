from django.urls import path

from task_manager.views import (
    index,
    TaskTypeListView,
    PositionListView,
    TeamListView,
    WorkerListView,
    ProjectListView,
    TaskListView,
)

urlpatterns = [
    path("", index, name="index"),
    path("task_types/", TaskTypeListView.as_view(), name="task_type-list"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("teams/", TeamListView.as_view(), name="team-list"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
]
app_name = "task_manager"
