from datetime import date
from django.test import TestCase
from django.urls import reverse

from projects.models import Project
from tasks.models import Task, TaskType
from workers.models import Worker, Position


class TaskModelTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")

        self.worker = Worker.objects.create_user(
            username="worker1",
            password="password123",
            position=self.position  # Передаємо об'єкт Position
        )
        self.project = Project.objects.create(name="Test Project")
        self.task_type = TaskType.objects.create(name="Feature")

        self.task = Task.objects.create(
            name="Implement Login",
            description="Create login page with Material Design",
            deadline=date(2026, 12, 31),
            is_completed=False,
            priority=Task.Priority.HIGH,
            task_type=self.task_type,
            project=self.project
        )
        self.task.assignees.add(self.worker)

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), "Feature")



    def test_task_relationships_and_defaults(self):
        self.assertEqual(self.task.name, "Implement Login")
        self.assertEqual(self.task.priority, Task.Priority.HIGH)
        self.assertFalse(self.task.is_completed)
        self.assertEqual(self.task.task_type, self.task_type)
        self.assertEqual(self.task.project, self.project)
        self.assertIn(self.worker, self.task.assignees.all())