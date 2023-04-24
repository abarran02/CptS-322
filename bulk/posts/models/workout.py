from django.db import models

from .post import Post


class Workout(Post):
    reps = models.IntegerField()
    time = models.DurationField(null=True, blank=True)
