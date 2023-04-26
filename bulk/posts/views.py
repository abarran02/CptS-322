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
    target_profile = get_object_or_404(User, pk=user_id)
    
    following = False
    user_requests_self = target_profile.id == request.user.id
    requesting_user_data = UserData.objects.get(user=request.user)
    # user is requesting another user's profile
    if not user_requests_self:
        # requesting user follows or unfollows the target profile
        if 'follow' in request.POST:
            requesting_user_data.following.add(target_profile)
        elif 'unfollow' in request.POST:
            requesting_user_data.following.remove(target_profile)

        # check whether requesting user is following target profile
        if not requesting_user_data.following.filter(id=target_profile.id).exists():
            following = True
        else:
            following = False
    
    profile_posts = Run.objects.filter(user=target_profile).order_by('-pub_date')

    return render(request, "details/profile.html", {
        "target_profile": target_profile,
        "following": following,
        "user_requests_self": user_requests_self,
        "requesting_user_data": requesting_user_data,
        "profile_posts": profile_posts
    })

@login_required
def post_detail(request: HttpRequest, post_id):
    # attempt to get requested post
    post_obj = get_object_or_404(Post, pk=post_id)
    # check that user has permission to view
    if post_obj.private and not post_obj.user.id == request.user.id:
        # otherwise return user to homepage
        return HttpResponseRedirect(reverse("home"))
    
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
        return render(request, "details/run_detail.html", {
            "post": post,
            "metric": user_data.metric,
            "run_map": post.gpx_map,
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
                private=request.POST["private"]=="on",
                user=request.user,
                gpx_upload=request.FILES["file"],
                calories_positive=False,
                post_type="run",
            )

            # get requesting user data to generate fitness stats and map
            user_data = UserData.objects.get(user=request.user)
            new_run.generate_stats_and_map(weight=user_data.weight, metric=user_data.metric)

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
                private=True,
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

        Workout.objects.create(
            title=workout_choice,
            pub_date=datetime.now(),
            private=False,
            post_type="workout",
            calories_positive=False,
            user=request.user,
            reps=number_reps
        )
    
        form = WorkoutForm(request.POST)
    
    return render(request, "create/workoutTracker.html", {
        "form":form,
        "workouts":dumps(workouts)
    })
