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
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            
            UserData.objects.update_or_create(
                height=form.cleaned_data['height'],
                weight=form.cleaned_data['weight'],
                metric=True,
                user=request.user
            )
            
            return HttpResponseRedirect(reverse('home'))

    # if a GET (or any other method) we'll create a blank form
    else:
        initial = {
            'first_name':request.user.first_name,
            'last_name':request.user.last_name,
            'email':request.user.email,
        }
        
        # attempt to get previous user data, ignore if not found
        try:
            user_data = UserData.objects.get(user=request.user)
            initial['height'] = user_data.height
            initial['weight'] = user_data.weight
        except ObjectDoesNotExist:
            pass
        
        form = SettingsForm(initial=initial)

    return render(request, 'settings.html', {'form': form})

@login_required
def login_redirect(request):
    # check user has logged in previously
    if not request.user.first_name:
        return HttpResponseRedirect(reverse('settings'))
    else:
        return HttpResponseRedirect(reverse('home'))
