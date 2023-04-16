# https://docs.python.org/3/library/unittest.html
# refrence to how to use unittest
import functools
import os
import sys
import unittest

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.test import TestCase

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from CalorieData import DrinkData, FoodData
from django.contrib.auth.models import User
from posts.models import Meal, Run


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

class MealTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='12345')
        Meal.objects.create(title="test", user=test_user)
        
    def test_sum_calories(self):
        meal = Meal.objects.get(title="test")
        meal.add_food("Chick-fil-A", "Spicy Chicken Sandwich")
        meal.add_food("Chick-fil-A", "Large Waffle Fries")
        meal.add_drink("Sprite")

        total_calories = meal.sum_calories()
        self.assertEqual(total_calories,1100)

class RunTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='12345')
        gpx_path = "media/uploads/sample.gpx"
        size = os.path.getsize(gpx_path)
        digest = TemporaryUploadedFile(gpx_path, 'text/plain', size, 'utf-8')
        Run.objects.create(title='sample', gpx_upload=digest, user=test_user)

    def test_distance(self):
        pass

    def test_calories(self):
        pass
    
if __name__ == "__main__":
    unittest.main()
