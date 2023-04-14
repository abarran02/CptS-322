# https://docs.python.org/3/library/unittest.html
# refrence to how to use unittest
import functools
import os
import sys
import unittest

from django.test import TestCase

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from CalorieData import DrinkData, FoodData
from posts.models import Meal

class testCases(unittest.TestCase):
    # test lookup of calorie data from FoodData and DrinkData
    def test_sum_calories(self):
        food_data = FoodData().calorie_lookup 
        drink_data = DrinkData().calorie_lookup
        
        meal = []
        # add two foods and one drink to meal
        meal.append(food_data["Chick-fil-A"]["Spicy Chicken Sandwich"])
        meal.append(food_data["Chick-fil-A"]["Large Waffle Fries"])
        meal.append(drink_data["Sprite"])

        total_calories = functools.reduce(lambda a,b: a + b, meal)
        self.assertEqual(total_calories,1100)

class ModelMealEntryTestCase(TestCase):
    def setUp(self):
        Meal.objects.create(title="test")
        
    def test_sum_calories(self):
        meal = Meal.objects.get(title="test")
        meal.add_food("Chick-fil-A", "Spicy Chicken Sandwich")
        meal.add_food("Chick-fil-A", "Large Waffle Fries")
        meal.add_drink("Sprite")
        
        total_calories = meal.sum_calories()
        self.assertEqual(total_calories,1100)
    
if __name__ == "__main__":
    unittest.main()
