from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import SettingsForm
from .models import UserData


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required
def settings(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SettingsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            handle_form(request.user, form.cleaned_data)
            return HttpResponseRedirect(reverse('home'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = init_form(request.user)

    return render(request, 'settings.html', {'form': form})

@login_required
def login_redirect(request):
    # check user has logged in previously
    if not request.user.first_name:
        return HttpResponseRedirect(reverse('settings'))
    else:
        return HttpResponseRedirect(reverse('home'))

def init_form(user) -> SettingsForm:
    """Populate SettingsForm with exising user data, if available. Blank otherwise."""
    initial = {
        'first_name':user.first_name,
        'last_name':user.last_name,
        'email':user.email,
    }
    
    # attempt to get previous user data, ignore if not found
    try:
        user_data = UserData.objects.get(user=user)
        initial['height'] = user_data.height
        initial['weight'] = user_data.weight
    except ObjectDoesNotExist:
        pass
    
    return SettingsForm(initial=initial)

def handle_form(user, cleaned_data):
    # update user info from form data
    user.first_name = cleaned_data['first_name']
    user.last_name = cleaned_data['last_name']
    user.email = cleaned_data['email']
    user.save()
    
    # update user's UserData object, or create if not yet created
    user_data = UserData.objects.update_or_create(
        user=user,
        defaults={
            'user':user,
            'height':cleaned_data['height'],
            'weight':cleaned_data['weight'],
            'metric': True,
            'location': cleaned_data['location']
        }
    )

    # force user to follow themself
    user_data[0].following.add(user)
