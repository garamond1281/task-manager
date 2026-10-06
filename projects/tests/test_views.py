from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from projects.models import Project
from tasks.models import Task, TaskType

User = get_user_model()


class ProjectViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testworker",
            password="testpassword123"
        )
        self.project = Project.objects.create(name="Alpha Project")

    def test_project_list_view_authenticated(self):
        self.client.login(username="testworker", password="testpassword123")
        response = self.client.get(reverse("projects:project_list"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.project, response.context["project_list"])
        self.assertTemplateUsed(response, "projects/project_list.html")
        self.assertIn("search_form", response.context)

    def test_project_list_view_unauthenticated(self):
        response = self.client.get(reverse("projects:project_list"))
        self.assertNotEqual(response.status_code, 200)

    def test_project_list_view_search(self):
        Project.objects.create(name="Beta Project")
        self.client.login(username="testworker", password="testpassword123")

        response = self.client.get(reverse("projects:project_list"), {"name": "Alpha"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.project, response.context["project_list"])
        self.assertEqual(len(response.context["project_list"]), 1)

    def test_project_detail_view(self):
        """Перевірка деталей проєкту та правильного підрахунку завдань у контексті"""
        self.client.login(username="testworker", password="testpassword123")
        task_type = TaskType.objects.create(name="Bug")

        Task.objects.create(
            name="Task 1",
            description="Desc 1",
            deadline="2026-12-31",
            is_completed=True,
            project=self.project,
            task_type=task_type
        )

        response = self.client.get(reverse("projects:project-detail", args=[self.project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["project"], self.project)
        self.assertEqual(response.context["num_completed"], 1)
        self.assertEqual(response.context["num_in_progress"], 0)

    def test_project_create_view_with_permission(self):
        perm = Permission.objects.get(codename="add_project")
        self.user.user_permissions.add(perm)
        self.client.login(username="testworker", password="testpassword123")
        response = self.client.post(reverse("projects:project_create"), {"name": "Gamma Project"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(name="Gamma Project").exists())

    def test_project_create_view_without_permission(self):
        self.client.login(username="testworker", password="testpassword123")
        response = self.client.get(reverse("projects:project_create"))
        self.assertIn(response.status_code, [302, 403])
        self.assertFalse(Project.objects.filter(name="Gamma Project").exists())