from django.conf import settings
from django.db import models


class Post(models.Model):
    """
    Parent model for Meal, Run, and Workout with the following data members:
    * title: CharField
    * pub_date: DateTimeField
    * calories: IntegerField
    * calories_positive: BooleanField (how to count towards total, burn vs consume)
    * user: ForeignKey
    """
    title = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField()

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
