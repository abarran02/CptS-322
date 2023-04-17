from CalorieData import DrinkData, FoodData
from django.db import models

food_data = FoodData()
drink_data = DrinkData()

class Food(models.Model):
    """Food model representing the title, description, and calories from a CalorieData lookup"""
    title = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    calories = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def data_from_food(self, restaurant: str, food: str):
        """Fill out title, description, and calories from a matching restaurant and food to CalorieData"""
        self.title = food
        self.description = restaurant
        self.calories = food_data.calorie_lookup[restaurant][food]
        self.save()

    def data_from_drink(self, drink: str):
        """Fill out title and calories from a matching drink to CalorieData"""
        self.calories = drink_data.calorie_lookup[drink]
        self.title = drink
        self.save()
