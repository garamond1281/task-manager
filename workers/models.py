from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('workers:worker-detail', args=[str(self.id)])