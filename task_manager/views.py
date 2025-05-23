from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView

from task_manager.forms import SignUpForm
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


class TaskTypeDetailView(LoginRequiredMixin, DetailView):
    model = TaskType
    template_name = "task_manager/task_type_detail.html"


class PositionListView(LoginRequiredMixin, ListView):
    model = Position
    template_name = "task_manager/position_list.html"


class PositionDetailView(LoginRequiredMixin, DetailView):
    model = Position
    template_name = "task_manager/position_detail.html"


class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = "task_manager/team_list.html"
    queryset = (
        Team.objects.prefetch_related("projects").prefetch_related("workers").all()
    )


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = "task_manager/team_detail.html"


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    template_name = "task_manager/worker_list.html"


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    template_name = "task_manager/worker_detail.html"


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "task_manager/project_list.html"


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "task_manager/project_detail.html"


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "task_manager/task_list.html"


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "task_manager/task_detail.html"
