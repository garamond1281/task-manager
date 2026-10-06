from datetime import date
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from projects.models import Project
from tasks.models import Task, TaskType
from workers.models import Position

User = get_user_model()


class TaskViewsTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.user = User.objects.create_user(
            username="taskmaster",
            password="securepassword123",
            position=self.position
        )
        self.project = Project.objects.create(name="Alpha Task Project")
        self.task_type = TaskType.objects.create(name="Feature")

        self.task = Task.objects.create(
            name="Implement Dashboard",
            description="Build dashboard UI",
            deadline=date(2026, 12, 31),
            is_completed=False,
            priority=Task.Priority.MEDIUM,
            task_type=self.task_type,
            project=self.project
        )
        self.task.assignees.add(self.user)

    def test_index_view_authenticated_and_session(self):
        self.client.login(username="taskmaster", password="securepassword123")

        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/index.html")
        self.assertEqual(response.context["num_workers"], 1)
        self.assertEqual(response.context["num_projects"], 1)
        self.assertEqual(response.context["num_tasks"], 1)
        self.assertEqual(response.context["num_visits"], 1)

        response_second = self.client.get(reverse("index"))
        self.assertEqual(response_second.context["num_visits"], 2)

    def test_index_view_unauthenticated(self):
        response = self.client.get(reverse("index"))
        self.assertNotEqual(response.status_code, 200)

    def test_task_list_view_filters(self):
        self.client.login(username="taskmaster", password="securepassword123")

        other_task_type = TaskType.objects.create(name="Bug")
        Task.objects.create(
            name="Fix Critical Bug",
            description="Fix login issue",
            deadline=date(2026, 12, 31),
            task_type=other_task_type,
            project=self.project
        )
        response = self.client.get(reverse("tasks:task_list"), {"name": "Dashboard"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.task, response.context["task_list"])
        self.assertEqual(len(response.context["task_list"]), 1)

        response_type = self.client.get(reverse("tasks:task_list"), {"task_type": self.task_type.id})
        self.assertEqual(response_type.status_code, 200)
        self.assertIn(self.task, response_type.context["task_list"])
        self.assertEqual(len(response_type.context["task_list"]), 1)

    def test_task_detail_view(self):
        self.client.login(username="taskmaster", password="securepassword123")
        response = self.client.get(reverse("tasks:task_detail", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["task"], self.task)

    def test_task_create_view_with_permission(self):
        perm = Permission.objects.get(codename="add_task")
        self.user.user_permissions.add(perm)
        self.client.login(username="taskmaster", password="securepassword123")

        form_data = {
            "name": "New Test Task",
            "description": "Testing creation",
            "deadline": "2026-12-31",
            "priority": "High",
            "task_type": self.task_type.id,
            "project": self.project.id,
            "assignees": [self.user.id],
            "is_completed": False
        }
        response = self.client.post(reverse("tasks:task_create"), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="New Test Task").exists())

    def test_task_create_view_without_permission(self):
        self.client.login(username="taskmaster", password="securepassword123")
        response = self.client.get(reverse("tasks:task_create"))
        self.assertIn(response.status_code, [302, 403])

    def test_task_delete_view_with_permission(self):
        perm = Permission.objects.get(codename="delete_task")
        self.user.user_permissions.add(perm)
        self.client.login(username="taskmaster", password="securepassword123")

        task_id = self.task.id
        response = self.client.post(reverse("tasks:task_delete", args=[task_id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=task_id).exists())