from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=255)


class Position(models.Model):
    name = models.CharField(max_length=255)


class Team(models.Model):
    name = models.CharField(max_length=255)


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, related_name="worker"
    )
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE, related_name="worker")


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE, related_name="project")


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
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=255, choices=PRIORITY_CHOICES, default=MEDIUM
    )
    task_type = models.ForeignKey(
        to=TaskType, on_delete=models.CASCADE, related_name="task"
    )
    assignees = models.ManyToManyField(to=Worker, related_name="tasks")
