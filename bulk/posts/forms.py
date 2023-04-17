from django import forms
from posts.models.run import Run

# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
class GPXForm(forms.Form):
    title = forms.CharField(max_length=64)
    file = forms.FileField()
