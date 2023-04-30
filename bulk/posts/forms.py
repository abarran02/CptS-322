from CalorieData import WorkoutData
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ModelForm
from posts.models import Food

# create list of tuples with format (choice, label)
workout_data = WorkoutData()
workout_choices = [ (workout, workout) for workout in workout_data.workout_list ]    
swim_choices = [ (swim, swim) for swim in workout_data.swim_list]

# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
class GPXForm(forms.Form):
    title = forms.CharField(max_length=64)
    file = forms.FileField()
    private = forms.BooleanField(required=False)

class WorkoutForm(forms.Form):
    title = forms.CharField(max_length=64)
    workout = forms.CharField(widget=forms.Select(choices=workout_choices))
    reps = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)])
    time = forms.DurationField(label="Time (HH:MM:SS)")
    private = forms.BooleanField(required=False)
    
class SwimWorkoutForm(forms.Form):
    stroke = forms.CharField(label="Stroke", widget=forms.Select(choices=swim_choices))
    time = forms.DurationField(label="Time (HH:MM:SS)")
    private = forms.BooleanField(required=False)
