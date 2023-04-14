from django.db import models
from .workout import Workout
from .meal import Meal

class Entry(models.Model):
    title = models.CharField(max_length=64)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, null=True, blank=True)
    fuel = models.ForeignKey(Meal, on_delete=models.CASCADE, null=True, blank=True)
    calories = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

    def calculate_net_calories(self):
        self.calories = self.food.calories - self.workout.calories
        self.save()
