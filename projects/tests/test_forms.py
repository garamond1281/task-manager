from django.test import TestCase
from projects.forms import ProjectSearchForm, ProjectForm


class ProjectFormsTests(TestCase):

    def test_project_search_form_valid(self):
        form_data = {"name": "Django"}
        form = ProjectSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Django")

    def test_project_search_form_empty(self):
        form = ProjectSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get("name", ""), "")

    def test_project_form_valid(self):
        form_data = {"name": "New Project"}
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())

        project = form.save()
        self.assertEqual(project.name, "New Project")
        self.assertIsNotNone(project.id)

    def test_project_form_invalid_missing_name(self):
        form_data = {"name": ""}
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)