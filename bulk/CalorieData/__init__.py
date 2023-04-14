import os
from json import loads

class FoodData:
    """
    Dataclass to ingest `foods.json` and provide the following data members:
    * all_data: raw JSON ingest as a list of dictionaries
    * calorie_lookup: dict of format { restaurant_name:{food_name:calories, ...}, ... } for
    fast calorie lookup given exact restaurant and food names
    * restaurants: list of all valid restaurants
    """
    def __init__(self):
        # get this file's directory to find foods.json
        json_path = os.path.join(os.path.dirname(__file__), 'foods.json')
        with open(json_path, 'r') as food_file:
            self.all_data = loads(food_file.read())

        # create nested dictionary of format above for easy calorie lookup
        self.calorie_lookup = {}
        for entry in self.all_data:
            restaurant_name = entry['restaurant']
            items_raw = entry['foodItems']
        
            # condense json object list to { food_name:calories, ... }
            items_clean = {}
            for item in items_raw:
                food_name = item['foodName']
                items_clean[food_name] = item['calories']

            self.calorie_lookup[restaurant_name] = items_clean
        
        # quick list of valid restaurants
        self.restaurants = self.calorie_lookup.keys()

        

class DrinkData:
    """
    Dataclass to ingest `drinks.json` and provide the following data members:
    * all_data: raw JSON ingest as a list of dictionaries
    * calorie_lookup: dict of format { drink_name:calories, ...} for
    fast calorie lookup given exact drink name
    """
    def __init__(self):
        # get this file's directory to find drinks.json
        json_path = os.path.join(os.path.dirname(__file__), 'drinks.json')
        with open(json_path, 'r') as drink_file:
            self.all_data = loads(drink_file.read())

        # create nested dictionary of format above for easy calorie lookup
        self.calorie_lookup = {}
        for entry in self.all_data:
            drink_name = entry['drinkName']
            calories = entry['calories']
            self.calorie_lookup[drink_name] = calories
