from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Case, When, IntegerField


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Task Type"
        verbose_name_plural = "Task Types"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Position"
        verbose_name_plural = "Positions"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position, on_delete=models.SET_NULL, related_name="workers", null=True
    )
    team = models.ForeignKey(
        to=Team, on_delete=models.SET_NULL, related_name="workers", null=True
    )

    class Meta:
        verbose_name = "Worker"
        verbose_name_plural = "Workers"
        ordering = ["username"]

    def __str__(self) -> str:
        return f"{self.username} {self.first_name} {self.last_name}"


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    teams = models.ManyToManyField(to=Team, related_name="projects")

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["deadline"]

    def __str__(self) -> str:
        return self.name


class TaskQuerySet(models.QuerySet):
    def priority_order(self):
        return self.annotate(
            priority_order=Case(
                When(priority="URGENT", then=1),
                When(priority="HIGH", then=2),
                When(priority="MEDIUM", then=3),
                When(priority="LOW", then=4),
                default=3,
                output_field=IntegerField(),
            )
        ).order_by("is_completed", "-deadline", "priority_order")


class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db).priority_order()


class Task(models.Model):
    URGENT = "URGENT"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    PRIORITY_CHOICES = (
        (URGENT, "Urgent"),
        (HIGH, "High"),
        (MEDIUM, "Medium"),
        (LOW, "Low"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=255, choices=PRIORITY_CHOICES, default=MEDIUM
    )
    task_type = models.ForeignKey(
        to=TaskType, on_delete=models.SET_NULL, related_name="tasks", null=True
    )
    project = models.ForeignKey(
        to=Project, on_delete=models.SET_NULL, related_name="tasks", null=True
    )
    assignees = models.ManyToManyField(to=Worker, related_name="tasks")

    objects = TaskManager()

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self) -> str:
        return f"{self.name} {self.priority}"
