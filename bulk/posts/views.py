from datetime import datetime
from json import dumps

from accounts.models import UserData
from CalorieData import FoodData, WorkoutData
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from posts.models import Meal, Post, Run, Workout

from .forms import FoodForm, GPXForm, WorkoutForm


def home(request: HttpRequest):
    if not request.user.is_authenticated:
        return render(request, "home_guest.html")
    else:
        # list of tuples with format (view, label)
        links = [
            ("user_index", "Users"),
            ("settings", "Settings"),
            ("add_meal", "Add Meal"),
            ("workout_tracker", "Workout Tracker"),
            ("logout", "Logout")
        ]
        # get list of users that logged in user is following
        user_data = UserData.objects.get(user=request.user)
        following = user_data.following.all()
        # get latest posts by following users
        latest_posts = Post.objects.filter(user__in=following).order_by('-pub_date')
        return render(request, "home.html", {
            "latest_posts": latest_posts,
            "links": links
        })

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

    return render(request, "details/profile.html", {
        "profile": profile,
        "user_data": user_data,
        "following": following,
        "user_is_self": user_is_self,
        "user_entries": user_entries
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
        return render(request, "details/meal_detail.html", {
            "post": post,
        })
    
    elif post_obj.post_type == "run":
        # get post_obj as a Run object
        post = Run.objects.get(pk=post_id)
        # update run stats and get plotly mapbox html
        run_map = post.generate_stats_and_map(weight=user_data.weight, metric=user_data.metric)

        return render(request, "details/run_detail.html", {
            "post": post,
            "metric": user_data.metric,
            "run_map": run_map
        })
    
    elif post_obj.post_type == "workout":
        # get post_obj as a Workout object
        post = Workout.objects.get(pk=post_id)
        return render(request, "details/workout_detail.html", {
            "post": post,
        })
    
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
                private=False,
                user=request.user,
                gpx_upload=request.FILES["file"],
                calories_positive=False,
                post_type="run",
            )
            return HttpResponseRedirect(reverse("detail", args=[new_run.id]))
    
    return render(request, "create/gpx_upload.html", {"form": form})

@login_required
def add_meal(request):
    resturants = FoodData().calorie_lookup
    if not request.method == "POST":
        form = FoodForm()
    else:
        form = FoodForm(request.POST)
        if form.is_valid:
            food_name = request.POST['display_foods']
            restaurant = request.POST['display_resturants']

            new_meal = Meal.objects.create(
                title=food_name,
                description=restaurant,
                pub_date=datetime.now(),
                private=False,
                post_type="meal",
                calories_positive=True,
                user=request.user
            )
            new_meal.add_food(restaurant, food_name)
            return HttpResponseRedirect(reverse("detail", args=[new_meal.id]))

    return render(request, "create/add_meal.html", {
        "form": form, 
        "restName": dumps(resturants)
    })

@login_required
def workout_tracker(request):
    workouts = WorkoutData().all_data # list of all string workouts
    if not request.method == "POST":
        form = WorkoutForm()
    else:    
        workout_choice = request.POST['workout_display']
        number_reps = request.POST['number_reps']

        new_workout = Workout.objects.create(
            title=workout_choice,
            pub_date=datetime.now(),
            private=False,
            post_type="workout",
            calories_positive=False,
            user=request.user,
            reps=number_reps
        )
    
        form = WorkoutForm(request.POST)
        return HttpResponseRedirect(reverse("detail", args=[new_workout.id]))
    
    return render(request, "create/workoutTracker.html", {
        "form":form,
        "workouts":dumps(workouts)
    })
