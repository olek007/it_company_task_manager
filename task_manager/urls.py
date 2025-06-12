from django.urls import path

from task_manager import views

urlpatterns = [
    path("", views.index, name="index"),
    path("task_types/", views.TaskTypeListView.as_view(), name="task_type-list"),
    path(
        "task_types/<int:pk>",
        views.TaskTypeDetailView.as_view(),
        name="task_type-detail",
    ),
    path(
        "task_types/create", views.TaskTypeCreateView.as_view(), name="task_type-create"
    ),
    path(
        "task_types/<int:pk>/update",
        views.TaskTypeUpdateView.as_view(),
        name="task_type-update",
    ),
    path(
        "task_types/<int:pk>/delete",
        views.TaskTypeDeleteView.as_view(),
        name="task_type-delete",
    ),
    path("positions/", views.PositionListView.as_view(), name="position-list"),
    path(
        "positions/<int:pk>", views.PositionDetailView.as_view(), name="position-detail"
    ),
    path(
        "positions/create", views.PositionCreateView.as_view(), name="position-create"
    ),
    path(
        "positions/<int:pk>/update",
        views.PositionUpdateView.as_view(),
        name="position-update",
    ),
    path(
        "positions/<int:pk>/delete",
        views.PositionDeleteView.as_view(),
        name="position-delete",
    ),
    path("teams/", views.TeamListView.as_view(), name="team-list"),
    path("teams/<int:pk>", views.TeamDetailView.as_view(), name="team-detail"),
    path("teams/create", views.TeamCreateView.as_view(), name="team-create"),
    path("teams/<int:pk>/update", views.TeamUpdateView.as_view(), name="team-update"),
    path("teams/<int:pk>/delete", views.TeamDeleteView.as_view(), name="team-delete"),
    path("workers/", views.WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>", views.WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create", views.WorkerCreateView.as_view(), name="worker-create"),
    path(
        "workers/<int:pk>/update",
        views.WorkerUpdateView.as_view(),
        name="worker-update",
    ),
    path(
        "workers/<int:pk>/delete",
        views.WorkerDeleteView.as_view(),
        name="worker-delete",
    ),
    path("projects/", views.ProjectListView.as_view(), name="project-list"),
    path("projects/<int:pk>", views.ProjectDetailView.as_view(), name="project-detail"),
    path("projects/create", views.ProjectCreateView.as_view(), name="project-create"),
    path(
        "projects/<int:pk>/update",
        views.ProjectUpdateView.as_view(),
        name="project-update",
    ),
    path(
        "projects/<int:pk>/delete",
        views.ProjectDeleteView.as_view(),
        name="project-delete",
    ),
    path("tasks/", views.TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>", views.TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create", views.TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update", views.TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete", views.TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/complete", views.task_set_completed, name="task-set_complete"),
    path(
        "tasks/<int:pk>/not-complete",
        views.task_set_not_completed,
        name="task-set_not_complete",
    ),
]
app_name = "task_manager"
