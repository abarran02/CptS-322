from datetime import datetime
from json import dumps

from accounts.models import UserData
from CalorieData import FoodData
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from posts.models import Food
from posts.models.run import Run

from .forms import FoodForm, GPXForm


def index(request: HttpRequest):
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

@login_required
def food_tracker(request):
    resturants = FoodData().calorie_lookup
    template = 'foodTracker.html'
    if (request.method == "POST"):
        food_Item_POST = request.POST['display_foods']
        resturant_Name_POST = request.POST['display_resturants']
        calories_NUM = resturants[resturant_Name_POST][food_Item_POST]
        #calories_POST = request.POST[calories_NUM]
        #Food.objects.create(title = food_Item_POST, description = resturant_Name_POST)
        new_Meal = Food(title= food_Item_POST, description= resturant_Name_POST, calories= calories_NUM)
        new_Meal.save()
       

        #.object.create()
        form = FoodForm(request.POST)
        #if form.is_valid(): 
            #return HttpResponseRedirect(reverse('home')) # returns home after submitting
    else:
        form = FoodForm()
    return render(request,  template, {"form":form,'restName': dumps(resturants)})
