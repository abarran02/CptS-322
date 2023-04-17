from django.conf import settings
from django.db import models


class UserData(models.Model):
    """Additional user attributes not included in the default User class"""
    
    # height and weight in cm and kg, respectively
    height = models.IntegerField()
    weight = models.IntegerField()
    metric = models.BooleanField()
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
