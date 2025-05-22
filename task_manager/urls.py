from django.urls import path

from task_manager.views import index, TaskTypeListView, PositionListView

urlpatterns = [
    path("", index, name="index"),
    path("taskType/", TaskTypeListView.as_view(), name="task_type_list"),
    path("position/", PositionListView.as_view(), name="position_list"),
]
app_name = "task_manager"
