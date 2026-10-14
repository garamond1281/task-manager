from django.test import TestCase
from django.urls import reverse

from projects.models import Project


class ProjectModelTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Django Task Manager")

    def test_project_str(self):
        self.assertEqual(str(self.project), "Django Task Manager")

    def test_project_absolute_url(self):
        expected_url = reverse('projects:project-detail', args=[str(self.project.id)])
        self.assertEqual(self.project.get_absolute_url(), expected_url)