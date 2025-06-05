from django.urls import reverse_lazy
from django.utils.http import urlencode

from task_manager.models import Task


class MyTasksFilterMixin:
    def get_queryset(self):
        queryset = (
            Task.objects.select_related("project")
            .select_related("task_type")
            .prefetch_related("assignees")
        )
        my_tasks = self.request.GET.get("my_tasks")
        if my_tasks:
            queryset = queryset.filter(assignees=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_tasks"] = self.request.GET.get("my_tasks")
        return context

    def get_success_url(self):
        base_url = reverse_lazy("task_manager:task-list")
        if self.request.GET.get("my_tasks"):
            return f"{base_url}?{urlencode({'my_tasks': 'True'})}"
        return base_url
