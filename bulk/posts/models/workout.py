from django.db import models

from .post import Post


class Workout(models.Model):
    reps = models.IntegerField()


class Workout(Post):
    time = models.DurationField(null=True, blank=True)
