from CalorieData import WorkoutData
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ModelForm
from posts.models import Food, SwimWorkout

# create list of tuples with format (choice, label)
workout_choices = []
for workout in WorkoutData().all_data:
    workout_choices.append( (workout, workout) )

# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
class GPXForm(forms.Form):
    title = forms.CharField(max_length=64)
    file = forms.FileField()
    private = forms.BooleanField(required=False)

class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ('title','description','calories')

class WorkoutForm(forms.Form):
    title = forms.CharField(max_length=64)
    workout = forms.CharField(widget=forms.Select(choices=workout_choices))
    reps = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)])
    private = forms.BooleanField(required=False)
    
class SwimWorkoutForm(ModelForm):
    class Meta:
        model = SwimWorkout
        fields = ('time','stroke')