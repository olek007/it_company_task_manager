from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
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


class TaskTypeListView(ListView):
    model = TaskType
    template_name = "task_manager/task_type_list.html"


class TaskTypeDetailView(DetailView):
    model = TaskType
    template_name = "task_manager/task_type_detail.html"


class PositionListView(ListView):
    model = Position
    template_name = "task_manager/position_list.html"


class PositionDetailView(DetailView):
    model = Position
    template_name = "task_manager/position_detail.html"


class TeamListView(ListView):
    model = Team
    template_name = "task_manager/team_list.html"
    queryset = (
        Team.objects.prefetch_related("projects").prefetch_related("workers").all()
    )


class WorkerListView(ListView):
    model = Worker
    template_name = "task_manager/worker_list.html"


class ProjectListView(ListView):
    model = Project
    template_name = "task_manager/project_list.html"


class TaskListView(ListView):
    model = Task
    template_name = "task_manager/task_list.html"
