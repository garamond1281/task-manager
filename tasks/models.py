from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from projects.models import Project
from workers.models import Worker


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "Urgent", "Urgent priority"
        HIGH = "High", "High priority"
        MEDIUM = "Medium", "Medium priority"
        LOW = "Low", "Low priority"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=Priority, default=Priority.MEDIUM)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, related_name="assigned_tasks")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('tasks:task_detail', args=[str(self.id)])
