from django.db import models
from projects.models import Project

# Create your models here.
class Task(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)
    completed=models.BooleanField(default=False)
    project=models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
