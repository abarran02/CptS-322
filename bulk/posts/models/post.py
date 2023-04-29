from datetime import timedelta

from django.conf import settings
from django.db import models


class Post(models.Model):
    """
    Parent model for Meal, Run, and Workout with the following data members:
    * title: CharField
    * description: TextField
    * pub_date: DateTimeField
    * private: BooleanField
    * post_type: CharField with choices "meal", "run", or "workout"
    * calories: IntegerField
    * calories_positive: BooleanField, how to count towards total, burn (-, False) vs consume (+, True)
    * user: ForeignKey for User model
    """
    title = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField()
    private = models.BooleanField()

    POST_TYPE_CHOICES = (
        ("meal", "Meal"),
        ("run", "Run"),
        ("workout", "Workout")
    )
    post_type = models.CharField(max_length=8, choices=POST_TYPE_CHOICES)

    calories = models.IntegerField(null=True, blank=True)
    calories_positive = models.BooleanField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

def calculate_calories_burned(MET: int, duration: timedelta, weight: int, metric: bool = True) -> float:
    """Calculate activity calories burned using the equation = MET * weight (kg) * time (hrs)"""
    # https://marathonhandbook.com/how-many-calories-burned-running-calculator/#met-formula
    if not metric:
        # convert kilograms to pounds
        weight /= 2.205
    return MET * weight * (duration.seconds / 3600)
