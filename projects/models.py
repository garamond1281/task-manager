from django.db import models
from django.urls import reverse


class Project(models.Model):
    name = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('projects:project-detail', args=[str(self.id)])

    def __str__(self):
        return self.name
