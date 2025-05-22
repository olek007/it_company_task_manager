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
    path("taskType/", TaskTypeListView.as_view(), name="task_type_list"),
    path("position/", PositionListView.as_view(), name="position_list"),
    path("team/", TeamListView.as_view(), name="team_list"),
    path("worker/", WorkerListView.as_view(), name="worker_list"),
    path("project/", ProjectListView.as_view(), name="project_list"),
    path("task/", TaskListView.as_view(), name="task_list"),
]
app_name = "task_manager"
