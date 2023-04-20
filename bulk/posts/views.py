from datetime import datetime

from accounts.models import UserData
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from posts.models import Meal, Post, Run, Workout

from .forms import GPXForm


def home(request: HttpRequest):
    if not request.user.is_authenticated:
        return render(request, "home_guest.html")
    else:
        # get list of users that logged in user is following
        user_data = UserData.objects.get(user=request.user)
        following = user_data.following.all()
        # get latest posts by following users
        latest_posts = Post.objects.filter(user__in=following).order_by('-pub_date')
        return render(request, "home.html", {"latest_posts": latest_posts})

@login_required
def user_index(request: HttpRequest):
    all_users = User.objects.all()
    return render(request, "user_index.html", {"all_users": all_users})

@login_required
def profile(request: HttpRequest, user_id):
    # get target user profile
    profile = get_object_or_404(User, pk=user_id)
    
    
    user_data = UserData.objects.get(user=request.user)
    user_is_self = profile.id == request.user.id # whether user is viewing their own profile
    # determine whether requetsing user 
    following = False
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
    
    profile_posts = Post.objects.filter(user=profile).order_by('-pub_date')

    return render(request, "profile.html", {
        "profile": profile,
        "user_data": user_data,
        "following": following,
        "user_is_self": user_is_self,
        "profile_posts": profile_posts
    })

@login_required
def post_detail(request: HttpRequest, post_id):
    # attempt to get requested post
    post_obj = get_object_or_404(Post, pk=post_id)
    user_data = UserData.objects.get(user=request.user)

    # determine post type and corresponding template to return
    if post_obj.post_type == "meal":
        # get post_obj as a Meal object
        post = Meal.objects.get(pk=post_id)
    
    elif post_obj.post_type == "run":
        # get post_obj as a Run object
        post = Run.objects.get(pk=post_id)
        # update run stats and get plotly mapbox html
        run_map = post.generate_stats_and_map(weight=user_data.weight, metric=user_data.metric)

        return render(request, "run_detail.html", {
            'post': post,
            'metric': user_data.metric,
            'run_map': run_map
        })
    
    elif post_obj.post_type == "workout":
        # get post_obj as a Workout object
        post = Workout.objects.get(pk=post_id)
    
    else:
        raise Http404("Post not found.")

@login_required
def gpx_form_upload(request: HttpRequest):
    if not request.method == "POST":
        form = GPXForm()
    else:
        form = GPXForm(request.POST, request.FILES)
        if form.is_valid():
            new_run = Run.objects.create(
                title=request.POST["title"],
                pub_date=datetime.now(),          
                user=request.user,
                gpx_upload=request.FILES["file"],
                calories_positive=False,
                post_type="run",
            )
            return HttpResponseRedirect(reverse("detail", args=[new_run.id]))
    
    return render(request, "gpx_upload.html", {"form": form})
