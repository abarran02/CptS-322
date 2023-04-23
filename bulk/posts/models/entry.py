from django.db import models
from .workout import Workout
from .meal import Meal

class Entry(models.Model):
    entry_id = models.IntegerField()
    title = models.CharField(max_length=64)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    fuel = models.ForeignKey(Meal, on_delete=models.CASCADE)
    calories = models.IntegerField()

    def __str__(self):
        return self.title

    def calculate_net_calories(self):
        self.calories = self.food.calories - self.workout.calories
