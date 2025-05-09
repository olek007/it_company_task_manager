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

admin.site.unregister(Group)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", "team")
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("position", "team")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Additional info", {"fields": ("position", "team")}),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "deadline", "team")


class WorkerInline(admin.TabularInline):
    model = Worker.tasks.through
    extra = 0
    show_change_link = True


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "deadline",
        "is_completed",
        "priority",
        "task_type",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "deadline",
                    "is_completed",
                    "priority",
                    "task_type",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "deadline",
                    "is_completed",
                    "priority",
                    "task_type",
                )
            },
        ),
    )
    inlines = [WorkerInline]
