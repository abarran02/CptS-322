from django.db import models
from .run import Run

class Workout(models.Model):
    description = models.TextField()
    run = models.ForeignKey(Run, on_delete=models.CASCADE, null=True, blank=True)
    calories = models.IntegerField(null=True, blank=True)

    def calories_manual(self, calories: int):
        self.calories = calories

    def calories_from_run(self, weight: int, metric: bool = True):
        self.run.generate_stats(weight, metric)
        self.calories = self.run.calories
        self.save()