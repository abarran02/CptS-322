from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from .food import Food
from .post import Post


class Meal(Post):
    """A set of Food objects"""
    food_items = models.ManyToManyField(Food)

    def __str__(self) -> str:
        return self.title

    def add_food(self, restaurant: str, food: str):
        """Add Food object to `food_items` by matching restaurant and food title """
        try:
            # filter all food objects by restaurant (case-insensitive)
            restaurant_match = Food.objects.filter(description__iexact=restaurant)
            # then match food title to Food object
            food_match = restaurant_match.get(title__iexact=food)
            self.food_items.add(food_match)

        # if Food does not exist yet
        except ObjectDoesNotExist:
            # create new object and add in one step
            new_food = self.food_items.create()
            new_food.data_from_food(restaurant, food)
            self.food_items.add(new_food)

        self.calories = self.sum_calories()
        self.save()

    def add_drink(self, drink: str):
        """Add Food object to `food_items` by matching drink title"""
        try:
            drink_match = Food.objects.get(title__iexact=drink)
            self.food_items.add(drink_match)
            
        except ObjectDoesNotExist:
            new_drink = self.food_items.create()
            new_drink.data_from_drink(drink)
            self.food_items.add(new_drink)

        self.calories = self.sum_calories()
        self.save()

    def sum_calories(self) -> int:
        """Returns the sum of calories from all Food objects in Meal"""
        calories = 0
        for food in self.food_items.all():
            calories += food.calories
            
        return calories
