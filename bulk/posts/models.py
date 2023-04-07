from django.db import models

class Run(models.Model):
    distance = models.FloatField()
    time = models.DurationField()
    calories = models.IntegerField()

class Workout(models.Model):
    description = models.TextField()
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    calories = models.IntegerField()
    
    def calories_manual(self, calories: int):
        self.calories = calories
    
    def calculate_calories_burned(self, weight: int, metric=False):
        self.calories = self.run.calculate_calories_burned(weight, metric)

class Food(models.Model):
    description = models.TextField()
    meal = models.CharField(max_length=32)
    calories = models.IntegerField()
    
    def calories_manual(self, calories: int):
        self.calories = calories
    
    def calculate_calories_consumed(self):
        food_data = {"Welch's Fruit Snack":45}
        self.calories = food_data[self.meal]

class Entry(models.Model):
    entry_id = models.IntegerField()
    title = models.CharField(max_length=64)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    fuel = models.ForeignKey(Food, on_delete=models.CASCADE)
    calories = models.IntegerField()
    
    def __str__(self):
        return self.title

    def calculate_net_calories(self):
        self.calories = self.food.calories - self.workout.calories
