from django.test import TestCase
from django.contrib.auth import get_user_model

from workers.forms import (
    WorkerSearchForm,
    WorkerCreationForm,
    UserRegisterForm,
)
from workers.models import Position

User = get_user_model()


class WorkerFormsTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Python Developer")

    def test_worker_search_form_valid_empty(self):
        form = WorkerSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get("first_name", ""), "")
        self.assertIsNone(form.cleaned_data.get("position"))

    def test_worker_search_form_with_data(self):
        form_data = {
            "first_name": "John",
            "position": self.position.id
        }
        form = WorkerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["first_name"], "John")
        self.assertEqual(form.cleaned_data["position"], self.position)

    def test_worker_creation_form_valid(self):
        form_data = {
            "username": "newworker",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
            "position": self.position.id
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user.username, "newworker")
        self.assertEqual(user.first_name, "Alice")
        self.assertEqual(user.last_name, "Smith")
        self.assertEqual(user.email, "alice@example.com")
        self.assertEqual(user.position, self.position)

    def test_bootstrap_form_mixin_and_register_form(self):
        form = UserRegisterForm()
        for field_name, field in form.fields.items():
            self.assertIn("form-control", field.widget.attrs.get("class", ""))

        form_data = {
            "username": "registeruser",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
            "email": "register@example.com"
        }
        reg_form = UserRegisterForm(data=form_data)
        self.assertTrue(reg_form.is_valid())

        user = reg_form.save()
        self.assertEqual(user.username, "registeruser")
        self.assertEqual(user.email, "register@example.com")