from django.db import models
from CalorieData import FoodData, DrinkData

food_data = FoodData()
drink_data = DrinkData()

class Run(models.Model):
    distance = models.FloatField()
    time = models.DurationField()
    calories = models.IntegerField()
    
    def calculate_calories_burned(self, weight: int, metric=False):
        # calories burned = MET * weight (kg) * time (hrs)
        # https://marathonhandbook.com/how-many-calories-burned-running-calculator/#met-formula
        if not metric:
            weight /= 2.205
        self.calories = 10 * weight * (self.time.seconds / 3600)

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
    meal = models.CharField(max_length=64)
    calories = models.IntegerField()
    
    def data_from_food(self, restaurant: str, food: str):
        self.calories = food_data[restaurant][food]
        self.meal = food
        self.description = f"from {restaurant}"
    
    def data_from_drink(self, drink: str):
        self.calories = drink_data[drink]
        self.meal = drink

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
