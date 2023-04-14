from django.db import models

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
