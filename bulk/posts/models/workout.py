from accounts.models import UserData
from django.db import models

from .post import Post, calculate_calories_burned


class Workout(Post):
    reps = models.IntegerField()
    time = models.DurationField(null=True, blank=True)

    def update_calories(self):
        user_data = UserData.objects.get(user=self.user)
        self.calories = calculate_calories_burned(5, self.time, user_data.weight, user_data.metric)

class Swim(Post):
    time = models.DurationField()
    
    def update_calories(self):
        user_data = UserData.objects.get(user=self.user)
        self.calories = calculate_calories_burned(7, self.time, user_data.weight, user_data.metric)
