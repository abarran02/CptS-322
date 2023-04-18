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


def home(request: HttpRequest):
    if request.user.is_authenticated:
        user_data = UserData.objects.get(user=request.user)
        following = user_data.following.all()
        latest_posts = Run.objects.filter(user__in=following).order_by('-pub_date')
    else:
        latest_posts = []
    return render(request, "home.html", {"latest_posts": latest_posts})

@login_required
def user_index(request: HttpRequest):
    all_users = User.objects.all()
    return render(request, "user_index.html", {"all_users": all_users})

@login_required
def profile(request: HttpRequest, user_id):
    # get target user profile
    profile = get_object_or_404(User, pk=user_id)
    
    following = False
    user_is_self = profile.id == request.user.id
    user_data = UserData.objects.get(user=request.user)
    if not user_is_self:
        # requesting user follows or unfollows the target profile
        if 'follow' in request.POST:
            user_data.following.add(profile)

        if 'unfollow' in request.POST:
            user_data.following.remove(profile)

        # check whether requesting user is following target profile
        if not user_data.following.filter(id=profile.id).exists():
            following = True
        else:
            following = False
    
    user_entries = Run.objects.filter(user=profile).order_by('-pub_date')

    return render(request, "profile.html", {
        "profile": profile,
        "user_data": user_data,
        "following": following,
        "user_is_self": user_is_self,
        "user_entries": user_entries
    })

@login_required
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
