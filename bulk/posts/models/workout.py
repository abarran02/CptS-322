from django.db import models
from .run import Run

class Workout(models.Model):
    description = models.TextField()
    pub_date = models.DateTimeField()
    calories = models.IntegerField(null=True, blank=True)
