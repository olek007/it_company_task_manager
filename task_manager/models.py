from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Task Type"
        verbose_name_plural = "Task Types"
        ordering = ["name"]


class Position(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Position"
        verbose_name_plural = "Positions"
        ordering = ["name"]


class Team(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        ordering = ["name"]


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, related_name="worker", null=True
    )
    team = models.ForeignKey(
        to=Team, on_delete=models.CASCADE, related_name="worker", null=True
    )

    class Meta:
        verbose_name = "Worker"
        verbose_name_plural = "Workers"
        ordering = ["username"]


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    team = models.ForeignKey(
        to=Team, on_delete=models.CASCADE, related_name="project", null=True
    )

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["deadline"]


class Task(models.Model):
    URGENT = "Urgent"
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
        to=TaskType, on_delete=models.CASCADE, related_name="task", null=True
    )
    assignees = models.ManyToManyField(to=Worker, related_name="tasks")

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["priority"]
