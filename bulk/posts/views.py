from datetime import datetime
from json import dumps

from accounts.models import UserData
from CalorieData import DrinkData, FoodData
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import (Http404, HttpRequest, HttpResponse,
                         HttpResponseRedirect)
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.dateparse import parse_duration
from posts.models import Meal, Post, Run, Swim, Workout

from .forms import GPXForm, SwimWorkoutForm, WorkoutForm


def render_with_navbar(request: HttpRequest, template: str, context) -> HttpResponse:
    context["links"] = [
        ("create_meal", "Meal"),
        ("create_workout", "Workout"),
        ("create_swim", "Swim"),
        ("create_run", "Run"),
    ]
    
    return render(request, template, context)

def home(request: HttpRequest):
    if not request.user.is_authenticated:
        return render(request, "home_guest.html")
    else:
        # list of tuples with format (view, label)

        # get list of users that logged in user is following
        user_data = UserData.objects.get(user=request.user)
        following = user_data.following.all()
        # get latest posts by following users
        latest_posts = Post.objects.filter(user__in=following).order_by('-pub_date')
        return render_with_navbar(request, "home.html", {
            "latest_posts": latest_posts,
        })

@login_required
def user_index(request: HttpRequest):
    all_users = User.objects.all()
    return render_with_navbar(request, "user_index.html", {"all_users": all_users})

def calories_today(user: User) -> int:
    profile_posts = Post.objects.filter(user=user).order_by('-pub_date')
    calories = 0
    for post in profile_posts:
        # only add calories burned today
        # break if subsequent posts are in the past
        if post.pub_date.date() == datetime.today().date():
            # only add calories burned, not consumed
            if not post.calories_positive:
                calories += post.calories
        else:
            break

    return calories

@login_required
def profile(request: HttpRequest, user_id):
    # get target user profile
    target_profile_user = get_object_or_404(User, pk=user_id)
    target_profile_data = get_object_or_404(UserData, user=target_profile_user)
    
    following = False
    user_requests_self = target_profile_user.id == request.user.id
    requesting_user_data = UserData.objects.get(user=request.user)
    # user is requesting another user's profile
    if not user_requests_self:
        # requesting user follows or unfollows the target profile
        if "follow" in request.POST:
            requesting_user_data.following.add(target_profile_user)
        elif "unfollow" in request.POST:
            requesting_user_data.following.remove(target_profile_user)

        # check whether requesting user is following target profile
        if not requesting_user_data.following.filter(id=target_profile_user.id).exists():
            following = True
        else:
            following = False

    profile_posts = Post.objects.filter(user=target_profile_user).order_by('-pub_date')

    return render_with_navbar(request, "details/profile.html", {
        "target_profile_user": target_profile_user,
        "target_profile_data": target_profile_data,
        "calories_burned_today": calories_today(target_profile_user),
        "following": following,
        "user_requests_self": user_requests_self,
        "requesting_user_data": requesting_user_data,
        "profile_posts": profile_posts
    })

def render_detail(request: HttpRequest, post_id: int, post_obj: Post, user_requests_self: bool):
    # determine post type and corresponding template to return
    if post_obj.post_type == "meal":
        # get post_obj as a Meal object
        post = Meal.objects.get(pk=post_id)
        template = "details/meal_detail.html"
    
    elif post_obj.post_type == "run":
        # get post_obj as a Run object
        post = Run.objects.get(pk=post_id)
        # update run stats and get plotly mapbox html
        template = "details/run_detail.html"
    
    elif post_obj.post_type == "workout":
        # get post_obj as a Workout object
        post = Workout.objects.get(pk=post_id)
        template = "details/workout_detail.html"
        
    elif post_obj.post_type == "swim":
        # get post_obj as a Swim object
        post = Swim.objects.get(pk=post_id)
        template = "details/swim_detail.html"

    else:
        raise Http404("Post not found.")
    
    return render_with_navbar(request, template, {
        "post": post,
        "user_requests_self": user_requests_self,
    })

@login_required
def post_detail(request: HttpRequest, post_id: int):
    # attempt to get requested post
    post_obj = get_object_or_404(Post, pk=post_id)
    # check that user has permission to view
    user_requests_self = post_obj.user == request.user
    if post_obj.private and not user_requests_self:
        # otherwise return user to homepage
        return HttpResponseRedirect(reverse("home"))
    
    # user deletes their own post
    if user_requests_self and "delete" in request.POST:
        post_obj.delete()
        return HttpResponseRedirect(reverse("home"))
   
    return render_detail(request, post_id, post_obj, user_requests_self)

@login_required
def create_run(request: HttpRequest):
    if not request.method == "POST":
        form = GPXForm()
    else:
        form = GPXForm(request.POST, request.FILES)
        if form.is_valid():
            private = request.POST.get("private", False)=="on"
            
            new_run = Run.objects.create(
                title=request.POST["title"],
                pub_date=datetime.now(),
                private=private,
                user=request.user,
                gpx_upload=request.FILES["file"],
                calories_positive=False,
                post_type="run",
            )

            # get requesting user data to generate fitness stats and map
            user_data = UserData.objects.get(user=request.user)
            new_run.generate_stats_and_map(weight=user_data.weight, metric=user_data.metric)

            return HttpResponseRedirect(reverse("detail", args=[new_run.id]))
    
    return render_with_navbar(request, "create/run.html", {"form": form})

@login_required
def create_meal(request):
    resturants = FoodData().calorie_lookup
    drinks = DrinkData().calorie_lookup
    if request.method == "POST":
        # also ensure that all fields were correctly filled
        # check restaurant first, as other fields will auto-populate once it is selected
        restaurant = request.POST.get("display_resturants", False)       
        if restaurant:
            food_name = request.POST.get("display_foods", False)
            drink = request.POST.get("display_drinks", False)

            # build title if drink was included
            title = food_name
            if drink != "None":
                title += f" and {drink}"

            new_meal = Meal.objects.create(
                title=title,
                description=restaurant,
                pub_date=datetime.now(),
                private=True,
                post_type="meal",
                calories_positive=True,
                user=request.user
            )
            new_meal.add_food(restaurant, food_name)
            new_meal.add_drink(drink)
            return HttpResponseRedirect(reverse("detail", args=[new_meal.id]))
        
    return render_with_navbar(request, "create/meal.html", {
        "restName": dumps(resturants),
        "drinksName": dumps(drinks)
    })

@login_required
def create_workout(request):
    if not request.method == "POST":
        form = WorkoutForm()
    else:
        form = WorkoutForm(request.POST)
        if form.is_valid():
            time = parse_duration(request.POST["time"])
            private = request.POST.get("private", False)=="on"

            new_workout = Workout.objects.create(
                title=request.POST["title"],
                description=request.POST["workout"],
                time=time,
                pub_date=datetime.now(),
                private=private,
                post_type="workout",
                calories_positive=False,
                user=request.user,
                reps=request.POST["reps"],
            )
            
            new_workout.update_calories()
            return HttpResponseRedirect(reverse("detail", args=[new_workout.id]))

    return render_with_navbar(request, "create/workout.html", {
        "form":form,
    })

@login_required
def create_swim(request):
    if not request.method == "POST":
        form = SwimWorkoutForm()
    else:
        form = SwimWorkoutForm(request.POST)
        if form.is_valid():
            time = parse_duration(request.POST["time"])
            private = request.POST.get("private", False)=="on"
            new_swim = Swim.objects.create(
                title=request.POST["stroke"],
                time=time,
                pub_date=datetime.now(),
                private=private,
                post_type="swim",
                calories_positive=False,
                user=request.user,
            )
            
            new_swim.update_calories()
            
            return HttpResponseRedirect(reverse("detail", args=[new_swim.id]))

    return render_with_navbar(request, "create/swim.html", {
        "form":form
    })
