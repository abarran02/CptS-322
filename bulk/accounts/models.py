from django.conf import settings
from django.db import models

class UserData(models.Model):
    """Additional user attributes not included in the default User class"""
    
    location = models.CharField(max_length=64, blank=True, null=True)

    # users that this user is following
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following')
    
    # height and weight in cm and kg, respectively
    height = models.IntegerField()
    weight = models.IntegerField()
    metric = models.BooleanField()

    daily_calories_goal = models.IntegerField()
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
