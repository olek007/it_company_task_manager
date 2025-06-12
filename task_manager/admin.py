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
    search_fields = ("name",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


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
    list_filter = ("is_superuser", "is_active")
    search_fields = UserAdmin.search_fields + ("first_name", "last_name")


class TeamInline(admin.TabularInline):
    model = Team.projects.through
    extra = 0
    show_change_link = True


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "deadline")
    search_fields = ("name", "description")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "deadline",
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
                )
            },
        ),
    )
    inlines = [TeamInline]


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
        "project",
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
                    "project",
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
                    "project",
                )
            },
        ),
    )
    inlines = [WorkerInline]
    list_filter = ("is_completed", "priority", "task_type")
    search_fields = ("name", "description")
