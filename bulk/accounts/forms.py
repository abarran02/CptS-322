from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ModelForm
from posts.models import Food, Workout


class SettingsForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=150)
    last_name = forms.CharField(label='Last name', max_length=150)
    email = forms.EmailField(label='Email')
    height = forms.IntegerField(label='Height (cm)', validators=[MinValueValidator(0), MaxValueValidator(250)])
    weight = forms.IntegerField(label='Weight (kg)', validators=[MinValueValidator(0), MaxValueValidator(250)])
    location = forms.CharField(label='Location', max_length=64)

class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = '__all__'
        #restruantDescription = forms.CharField(label="Restraunt")

class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        #fields = '__all__'
        fields = ('description', 'reps')
