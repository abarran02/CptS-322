from django.db import models
from CalorieData import FoodData, DrinkData
from functools import reduce

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
#Model for Meal

class MealEntry(models.Model):
    #refernce
    #https://stackoverflow.com/questions/1110153/what-is-the-most-efficient-way-to-store-a-list-in-the-django-models

    #Meal type either breakfast, lunch, dinner, or snack
    mealType = models.CharField(max_length=10) 
    #Idea: For now we will use a list, later on will figure out how to incorrporste a listField for SQL database storage
    entireMeal = []
    totalCaloriesForMeal = models.IntegerField()

    #Fucntions for this class later on
    #def __init__(self, *args: Any, **kwargs: Any) -> None: #will figure this out later
        #super().__init__(*args, **kwargs)

    def __init__(self):
        self.mealType = ""
        self.entireMeal = []
    
    """
    Functions maybe used later on to verify that our Meal type is of a valid type
    """
    def setMealType(self, newMealType):
        if not isinstance(self.mealType, models.CharField):
            return False
        else:
            if (newMealType.upper() == "BREAKFAST") or (newMealType.upper() == "LUNCH") or (newMealType.upper() == "DINNER") or (newMealType.upper() == "SNACK"):
                self.mealType = newMealType
            else:
                return False
    
    """
    Adds meal item to list then sums list again
    """
    def addMealItem(self, newItem):
        if len(self.entireMeal) > 0:
            self.entireMeal.append(newItem)
            self.totalCaloriesForMeal = reduce(lambda a,b: a + b, self.entireMeal)

    def getTotalCalories(self):
        if len(self.entireMeal) > 0:
            print(f"Total Calories for meal is: {self.totalCaloriesForMeal}")
            return self.totalCaloriesForMeal
        return None

    


