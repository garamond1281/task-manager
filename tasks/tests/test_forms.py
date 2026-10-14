from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model

from tasks.forms import TaskSearchForm, TaskForm
from tasks.models import TaskType
from projects.models import Project
from workers.models import Position

User = get_user_model()


class TaskFormsTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = User.objects.create_user(
            username="testworker",
            password="password123",
            position=self.position
        )
        self.project = Project.objects.create(name="Test Project")
        self.task_type = TaskType.objects.create(name="Bug Fix")

    def test_task_search_form_valid_empty(self):
        form = TaskSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get("name", ""), "")
        self.assertIsNone(form.cleaned_data.get("task_type"))

    def test_task_search_form_with_data(self):
        form_data = {
            "name": "Login bug",
            "task_type": self.task_type.id
        }
        form = TaskSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Login bug")
        self.assertEqual(form.cleaned_data["task_type"], self.task_type)

    def test_task_form_valid(self):
        form_data = {
            "name": "Fix authentication error",
            "description": "Users cannot log in via CSRF token",
            "deadline": date(2026, 12, 31),
            "priority": "High",
            "task_type": self.task_type.id,
            "project": self.project.id,
            "assignees": [self.worker.id],
            "is_completed": False
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

        task = form.save()
        self.assertEqual(task.name, "Fix authentication error")
        self.assertIn(self.worker, task.assignees.all())
        self.assertEqual(task.project, self.project)
        self.assertEqual(task.task_type, self.task_type)

    def test_task_form_missing_assignees(self):
        form_data = {
            "name": "Fix authentication error",
            "description": "Desc",
            "deadline": date(2026, 12, 31),
            "priority": "High",
            "task_type": self.task_type.id,
            "project": self.project.id,
            "assignees": [],
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("assignees", form.errors)