from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

class SettingsForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=150)
    last_name = forms.CharField(label='Last name', max_length=150)
    email = forms.EmailField(label='Email')
    height = forms.IntegerField(label='Height (cm)', validators=[MinValueValidator(0), MaxValueValidator(250)])
    weight = forms.IntegerField(label='Weight (kg)', validators=[MinValueValidator(0), MaxValueValidator(250)])
