from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)

from task_manager.forms import (
    SignUpForm,
    WorkerCreateForm,
    ProjectForm,
    TaskForm,
    WorkerUpdateForm,
)
from task_manager.models import TaskType, Position, Team, Worker, Project, Task


@login_required
def index(request):
    return render(request, "task_manager/index.html")


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = "/"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class TaskTypeListView(LoginRequiredMixin, ListView):
    model = TaskType
    template_name = "task_manager/task_type_list.html"
    context_object_name = "task_type_list"


class TaskTypeDetailView(LoginRequiredMixin, DetailView):
    model = TaskType
    template_name = "task_manager/task_type_detail.html"
    context_object_name = "task_type"


class TaskTypeCreateView(LoginRequiredMixin, CreateView):
    model = TaskType
    template_name = "task_manager/task_type_form.html"
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task_type-list")
    context_object_name = "task_type"


class TaskTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskType
    template_name = "task_manager/task_type_form.html"
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task_type-list")
    context_object_name = "task_type"


class TaskTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskType
    template_name = "task_manager/task_type_confirm_delete.html"
    success_url = reverse_lazy("task_manager:task_type-list")
    context_object_name = "task_type"


class PositionListView(LoginRequiredMixin, ListView):
    model = Position
    template_name = "task_manager/position_list.html"


class PositionDetailView(LoginRequiredMixin, DetailView):
    model = Position
    template_name = "task_manager/position_detail.html"


class PositionCreateView(LoginRequiredMixin, CreateView):
    model = Position
    template_name = "task_manager/position_form.html"
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionUpdateView(LoginRequiredMixin, UpdateView):
    model = Position
    template_name = "task_manager/position_form.html"
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionDeleteView(LoginRequiredMixin, DeleteView):
    model = Position
    template_name = "task_manager/position_confirm_delete.html"
    success_url = reverse_lazy("task_manager:position-list")


class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = "task_manager/team_list.html"
    queryset = (
        Team.objects.prefetch_related("projects").prefetch_related("workers").all()
    )


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = "task_manager/team_detail.html"
    queryset = (
        Team.objects.prefetch_related("projects").prefetch_related("workers").all()
    )


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    template_name = "task_manager/team_form.html"
    fields = "__all__"
    success_url = reverse_lazy("task_manager:team-list")


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    template_name = "task_manager/team_form.html"
    fields = "__all__"
    success_url = reverse_lazy("task_manager:team-list")


class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = "task_manager/team_confirm_delete.html"
    success_url = reverse_lazy("task_manager:team-list")


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    template_name = "task_manager/worker_list.html"
    queryset = Worker.objects.select_related("team").prefetch_related("tasks").all()


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    template_name = "task_manager/worker_detail.html"
    queryset = Worker.objects.select_related("team").prefetch_related("tasks").all()


class WorkerCreateView(LoginRequiredMixin, CreateView):
    form_class = WorkerCreateForm
    template_name = "task_manager/worker_form.html"
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    template_name = "task_manager/worker_form.html"
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerDeleteView(LoginRequiredMixin, DeleteView):
    model = Worker
    template_name = "task_manager/worker_confirm_delete.html"
    success_url = reverse_lazy("task_manager:worker-list")


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "task_manager/project_list.html"
    queryset = Project.objects.select_related("team").prefetch_related("tasks").all()


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "task_manager/project_detail.html"
    queryset = Project.objects.select_related("team").prefetch_related("tasks").all()


class ProjectCreateView(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = "task_manager/project_form.html"
    success_url = reverse_lazy("task_manager:project-list")


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "task_manager/project_form.html"
    success_url = reverse_lazy("task_manager:project-list")


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "task_manager/task_list.html"
    queryset = (
        Task.objects.select_related("project").prefetch_related("assignees").all()
    )


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "task_manager/task_detail.html"
    queryset = (
        Task.objects.select_related("project").prefetch_related("assignees").all()
    )


class TaskCreateView(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = "task_manager/task_form.html"
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_manager/task_form.html"
    success_url = reverse_lazy("task_manager:task-list")
