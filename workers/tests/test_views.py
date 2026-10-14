from datetime import date
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from projects.models import Project
from tasks.models import Task, TaskType
from workers.models import Position, Worker

User = get_user_model()


class WorkerViewsTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Software Engineer")

        self.admin_user = User.objects.create_superuser(
            username="adminworker",
            password="adminpassword123",
            position=self.position
        )
        self.regular_user = User.objects.create_user(
            username="regularworker",
            password="password123",
            first_name="Jane",
            position=self.position
        )

        self.project = Project.objects.create(name="Worker Test Project")
        self.task_type = TaskType.objects.create(name="Task")

        self.completed_task = Task.objects.create(
            name="Completed Task",
            description="Done",
            deadline=date(2026, 12, 31),
            is_completed=True,
            task_type=self.task_type,
            project=self.project
        )
        self.completed_task.assignees.add(self.regular_user)

    def test_worker_list_view_authenticated(self):
        self.client.login(username="adminworker", password="adminpassword123")
        response = self.client.get(reverse("workers:worker-list"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.regular_user, response.context["worker_list"])
        self.assertTemplateUsed(response, "workers/worker_list.html")
        self.assertIn("search_form", response.context)

    def test_worker_list_view_search_filters(self):
        self.client.login(username="adminworker", password="adminpassword123")

        response = self.client.get(reverse("workers:worker-list"), {"first_name": "Jane"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.regular_user, response.context["worker_list"])
        self.assertEqual(len(response.context["worker_list"]), 1)

        response_pos = self.client.get(reverse("workers:worker-list"), {"position": self.position.id})
        self.assertEqual(response_pos.status_code, 200)
        self.assertIn(self.regular_user, response_pos.context["worker_list"])

    def test_worker_detail_view(self):
        self.client.login(username="adminworker", password="adminpassword123")
        response = self.client.get(reverse("workers:worker-detail", args=[self.regular_user.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["worker"], self.regular_user)
        self.assertEqual(response.context["num_completed"], 1)
        self.assertEqual(response.context["num_in_progress"], 0)
        self.assertIn(self.completed_task, response.context["completed_list"])

    def test_worker_create_view_with_permission(self):
        perm = Permission.objects.get(codename="add_worker")
        self.admin_user.user_permissions.add(perm)
        self.client.login(username="adminworker", password="adminpassword123")

        form_data = {
            "username": "brandnewworker",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "first_name": "Mark",
            "last_name": "Twain",
            "email": "mark@example.com",
            "position": self.position.id
        }
        response = self.client.post(reverse("workers:worker-create"), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Worker.objects.filter(username="brandnewworker").exists())

    def test_worker_delete_view_with_permission(self):
        perm = Permission.objects.get(codename="delete_worker")
        self.admin_user.user_permissions.add(perm)
        self.client.login(username="adminworker", password="adminpassword123")

        user_id = self.regular_user.id
        response = self.client.post(reverse("workers:worker-delete", args=[user_id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Worker.objects.filter(id=user_id).exists())

    @patch("workers.services.user_service.UserService.register_user")
    def test_user_register_view(self, mock_register_user):
        form_data = {
            "username": "guestuser",
            "password1": "GuestPass123!",
            "password2": "GuestPass123!",
            "email": "guest@example.com"
        }
        response = self.client.post(reverse("register"), data=form_data)
        self.assertRedirects(response, reverse("login"))
        mock_register_user.assert_called_once()