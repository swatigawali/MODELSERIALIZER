from django.db import models
from django.db.models.base import Model

# Create your models here.
class Task(models.Model):
    title=models.CharField(max_length=20)
    description=models.CharField(max_length=100)
    completed=models.BooleanField()

    def __str__(self):
        return self.title