from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from posts.models.run import Run

from .forms import GPXForm


def index(request):
    return HttpResponse("Hello, world. You're at the Posts index.")

@login_required
def gpx_form_upload(request: HttpRequest):
    if request.method == "POST":
        form = GPXForm(request.POST, request.FILES)
        if form.is_valid():
            Run.objects.create(title=request.POST["title"], 
                      user=request.user, 
                      gpx_upload=request.FILES["file"]
            )
            return HttpResponseRedirect(reverse("home"))
    else:
        form = GPXForm()

    return render(request, "gpx_upload.html", {
        "form": form
    })
