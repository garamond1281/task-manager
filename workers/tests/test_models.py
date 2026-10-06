from django.test import TestCase
from django.urls import reverse
from workers.models import Position, Worker


class WorkerModelTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Backend Developer")

        self.worker = Worker.objects.create_user(
            username="johndoe",
            password="securepassword123",
            first_name="John",
            last_name="Doe",
            position=self.position
        )

    def test_position_str(self):
        self.assertEqual(str(self.position), "Backend Developer")

    def test_worker_str(self):
        self.assertEqual(str(self.worker), "johndoe")

    def test_worker_absolute_url(self):
        expected_url = reverse("workers:worker-detail", args=[str(self.worker.id)])
        self.assertEqual(self.worker.get_absolute_url(), expected_url)

    def test_worker_fields_and_position_relationship(self):
        self.assertEqual(self.worker.username, "johndoe")
        self.assertEqual(self.worker.first_name, "John")
        self.assertEqual(self.worker.last_name, "Doe")
        self.assertEqual(self.worker.position, self.position)