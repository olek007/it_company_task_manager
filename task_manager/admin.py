from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.models import Group

from task_manager.models import (
    Position,
    TaskType,
    Team,
    Worker,
    Project,
    Task,
)

# Register your models here.

admin.site.unregister(Group)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", "team")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "deadline", "team")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "deadline",
        "is_completed",
        "priority",
        "task_type",
    )
