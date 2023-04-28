from django.db import models

from .post import Post


class Workout(Post):
    # Should we add a third field for description of exercise and swim stroke
    #exercise = models.CharField(max_length=100)
    reps = models.IntegerField()
    time = models.DurationField(null=True, blank=True)

class SwimWorkout(Post):
    time = models.DurationField(null=True, blank=True)
    stroke = models.CharField(max_length=100)