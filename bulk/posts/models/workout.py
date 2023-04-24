from django.db import models
from .run import Run

class Workout(models.Model):
    description = models.TextField()
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    calories = models.IntegerField()
    reps = models.IntegerField()

    def calories_manual(self, calories: int):
        self.calories = calories

    def calculate_calories_burned(self, weight: int, metric=False):
        self.calories = self.run.calculate_calories_burned(weight, metric)
