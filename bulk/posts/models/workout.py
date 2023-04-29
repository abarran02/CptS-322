from django.db import models

from .post import Post, calculate_calories_burned


class Workout(Post):
    reps = models.IntegerField()
    time = models.DurationField(null=True, blank=True)

    def update_calories(self, weight: int, metric: bool = True):
        duration = self.time
        self.calories = calculate_calories_burned(5, duration, weight, metric)

class SwimWorkout(Post):
    time = models.DurationField(null=True, blank=True)
