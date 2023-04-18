from datetime import datetime

from accounts.models import UserData
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from posts.models.run import Run

from .forms import GPXForm


def user_index(request: HttpRequest):
    all_users = User.objects.all()
    return render(request, "user_index.html", {"all_users": all_users})

def profile(request: HttpRequest, user_id):
    # get target user profile
    profile = get_object_or_404(User, pk=user_id)
    
    # requesting user follows or unfollows the target profile
    user_data = UserData.objects.get(user=request.user)
    if 'follow' in request.POST:
        user_data.following.add(profile)
    
    if 'unfollow' in request.POST:
        user_data.following.remove(profile)
    
    # check whether requesting user is following target profile
    if not user_data.following.filter(id=profile.id).exists():
        following = True
    else:
        following = False
    
    return render(request, "profile.html", {"profile": profile, "following": following})

def run_index(request: HttpRequest):
    latest_posts = Run.objects.filter(user=request.user).order_by('-pub_date')
    return render(request, "index.html", {"latest_posts": latest_posts})

def detail(request: HttpRequest, post_id):
    post = get_object_or_404(Run, pk=post_id)
    user_data = UserData.objects.get(user=request.user)
    run_map = post.generate_stats_and_map(weight=user_data.weight, metric=user_data.metric)

    return render(request, "run_detail.html", {
        'post': post,
        'metric': user_data.metric,
        'run_map': run_map
    })

@login_required
def gpx_form_upload(request: HttpRequest):
    if request.method == "POST":
        form = GPXForm(request.POST, request.FILES)
        if form.is_valid():
            Run.objects.create(
                title=request.POST["title"],
                pub_date=datetime.now(),          
                user=request.user,
                gpx_upload=request.FILES["file"]
            )
            return HttpResponseRedirect(reverse("home"))
    else:
        form = GPXForm()

    return render(request, "gpx_upload.html", {"form": form})
