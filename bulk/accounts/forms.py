from django import forms
from django.forms import ModelForm
from posts.models import Food

#test_list = [1,2,3]

class SettingsForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=150)
    last_name = forms.CharField(label='Last name', max_length=150)
    email = forms.EmailField(label='Email')

"""
class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ('title')
        #fields = '__all__'
        widgetDropDown = forms.Select(choices=test_list)    
"""

        
