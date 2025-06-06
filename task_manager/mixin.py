from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.http import urlencode

from task_manager.forms import NameSearchForm
from task_manager.models import Task


class MyTasksFilterMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        my_tasks = self.request.GET.get("my_tasks")
        if my_tasks == "True":
            queryset = queryset.filter(assignees=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_tasks"] = self.request.GET.get("my_tasks")
        return context

    def get_success_url(self):
        base_url = reverse_lazy("task_manager:task-list")
        query_params = {}
        if self.request.GET.get("my_tasks"):
            query_params["my_tasks"] = "True"
        if self.request.GET.get("name"):
            query_params["name"] = self.request.GET["name"]
        if query_params:
            return f"{base_url}?{urlencode(query_params)}"
        return base_url


class SearchBarMixin:
    search_fields = ["name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["search_form"] = NameSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = NameSearchForm(self.request.GET)
        if form.is_valid():
            search_query = form.cleaned_data["name"]
            if search_query:
                queries = Q()
                for field in self.search_fields:
                    queries |= Q(**{f"{field}__icontains": search_query})
                queryset = queryset.filter(queries)
        return queryset
