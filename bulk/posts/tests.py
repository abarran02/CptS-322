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

#Idea: Class for Meals of the day such as Breakfast, Lunch, Dinner, and snacks

#class Meal():
    #def __init__(self) -> None:
        
"""
# Create your tests here.
class testCases(unittest.TestCase): 
    #Calculations for calories of FoodData
    def testAddCalories(self):
        food_dataDict = FoodData().calorie_lookup 
        drink_dataDict = DrinkData().calorie_lookup

        testMeal:list = []
        # Idea: maybe create a list with value of meal to later add like myfitnesspal

        testSpicyChickenCalories = food_dataDict["Chick-fil-A"]["Spicy Chicken Sandwich"]
     
        testSpriteCalories = drink_dataDict["Sprite"]

        testLargeFries = food_dataDict["Chick-fil-A"]["Large Waffle Fries"]
        print(f"Chick-Fil-A meal calories: Spicy Chicken Sandwich: {testSpicyChickenCalories}, Large Fries {testLargeFries}, and Medium Sprite {testSpriteCalories}")

        testMeal.append(testSpicyChickenCalories)
        testMeal.append(testLargeFries)
        testMeal.append(testSpriteCalories)

        totalCalories = functools.reduce(lambda a,b: a + b, testMeal)
        print(totalCalories)
        #self.assertEqual(totalCalories,)
"""
        
if __name__ == "__main__":
    #unittest.main()
    food_dataDict = FoodData().calorie_lookup 
    drink_dataDict = DrinkData().calorie_lookup

    testMeal:list = []
        # Idea: maybe create a list with value of meal to later add like myfitnesspal

    testSpicyChickenCalories = food_dataDict["Chick-fil-A"]["Spicy Chicken Sandwich"]
     
    testSpriteCalories = drink_dataDict["Sprite"]

    testLargeFries = food_dataDict["Chick-fil-A"]["Large Waffle Fries"]
    print(f"Chick-Fil-A meal calories: Spicy Chicken Sandwich: {testSpicyChickenCalories}, Large Fries {testLargeFries}, and Medium Sprite {testSpriteCalories}")

    testMeal.append(testSpicyChickenCalories)
    testMeal.append(testLargeFries)
    testMeal.append(testSpriteCalories)

    totalCalories = functools.reduce(lambda a,b: a + b, testMeal)
    print(totalCalories)


