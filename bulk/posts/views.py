from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from posts.models.run import Run

from .forms import GPXForm


def index(request):
    latest_posts = Run.objects.all()
    return render(request, "index.html", {"latest_posts": latest_posts})

def detail(request, post_id):
    post = get_object_or_404(Run, pk=post_id)
    return render(request, "run_detail.html", {'post': post})

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

    return render(request, "gpx_upload.html", {"form": form})
