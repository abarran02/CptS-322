from django import forms
from django.forms import ModelForm
from posts.models import Food, Workout


# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
class GPXForm(forms.Form):
    title = forms.CharField(max_length=64)
    file = forms.FileField()

class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ('title','description','calories')

class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ('description', 'reps')
