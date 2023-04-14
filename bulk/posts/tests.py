from django.test import TestCase
import unittest
# https://docs.python.org/3/library/unittest.html
# refrence to how to use unittest
import functools 
import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from CalorieData import FoodData, DrinkData
from posts.models import Meal
#Idea: Class for Meals of the day such as Breakfast, Lunch, Dinner, and snacks

#class Meal():
    #def __init__(self) -> None:
    #mkae a model for this


# Create your tests here.
class testCases(unittest.TestCase): 

    #Calculations for calories of FoodData
    """
    This first tests case just adds onto a list made in the function
    """
    def testAddCalories(self):
        food_dataDict = FoodData().calorie_lookup 
        drink_dataDict = DrinkData().calorie_lookup

        testMeal:list = []
        # Idea: maybe create a list with value of meal to later add like myfitnesspal

        testSpicyChickenCalories = food_dataDict["Chick-fil-A"]["Spicy Chicken Sandwich"]
     
        testSpriteCalories = drink_dataDict["Sprite"]

        testLargeFries = food_dataDict["Chick-fil-A"]["Large Waffle Fries"]
        #print(f"Chick-Fil-A meal calories: Spicy Chicken Sandwich: {testSpicyChickenCalories}, Large Fries {testLargeFries}, and Medium Sprite {testSpriteCalories}")

        """
        Will later append this to a list of meal Model Class in posts.models.py
        """
        testMeal.append(testSpicyChickenCalories)
        testMeal.append(testLargeFries)
        testMeal.append(testSpriteCalories)

        totalCalories = functools.reduce(lambda a,b: a + b, testMeal)
        #print(totalCalories)
        self.assertEqual(totalCalories,1100)

    """
    This tests case same as the first,but implementsing our model class mealEntry()
    """


class ModelMealEntryTestCase(TestCase):
    
    def testAddCalories2(self):
        food_dataDict = FoodData().calorie_lookup 
        drink_dataDict = DrinkData().calorie_lookup

        testSpicyChickenCalories = food_dataDict["Chick-fil-A"]["Spicy Chicken Sandwich"]
        testSpriteCalories = drink_dataDict["Sprite"]
        testLargeFries = food_dataDict["Chick-fil-A"]["Large Waffle Fries"]

        newMeal = Meal.objects.create(newMealType = "Breakfast", food1 = testSpicyChickenCalories, 
                                      food2 = testSpriteCalories, food3 = testLargeFries)
        newMeal = Meal.objects.aaggregate()
        
        
    def testAddCalories(self):
        food_dataDict = FoodData().calorie_lookup 
        drink_dataDict = DrinkData().calorie_lookup
        #mealList = MealEntry()
        
        
        #mealList.mealType = "Breakfast"
        testSpicyChickenCalories = food_dataDict["Chick-fil-A"]["Spicy Chicken Sandwich"]
        testSpriteCalories = drink_dataDict["Sprite"]
        testLargeFries = food_dataDict["Chick-fil-A"]["Large Waffle Fries"]

       # mealList.getTotalCalories()
       # self.assertEqual(mealList.getTotalCalories, None)
       # mealList.addMealItem(testSpicyChickenCalories)
       # mealList.getTotalCalories()
       # mealList.addMealItem(testSpriteCalories)
       # mealList.getTotalCalories()
       # mealList.addMealItem(testLargeFries)
       # mealList.getTotalCalories()
       # self.assertEqual(mealList.getTotalCalories,1100)

    
if __name__ == "__main__":
    unittest.main()
