from django.shortcuts import render, redirect
from .models import Profile, Tweet
from django.contrib import messages
from .forms import TweetForm


def home(request):
    tweets = Tweet.objects.all().order_by("-created_at")
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, "Your tweet added successfully!")
                return redirect("home")
        return render(request, "home.html", {"tweets": tweets, "form": form})
    else:
        return render(request, "home.html", {"tweets", tweets})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, "profile_list.html", {"profiles": profiles})
    else:
        messages.info(request, "Log in to view the page")
        return redirect("home")


def profile(request, pk):
    if request.user.is_authenticated:
        u_profile = Profile.objects.get(user_id=pk)
        user_tweets = Tweet.objects.filter(user_id=pk).order_by("-created_at")
        # post form logic
        if request.method == "POST":
            # GET current user ID
            current_user_profile = request.user.profile
            # get form date
            action = request.POST["follow"]
            # decide to follow or not
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            else:
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        context = {
            "profile": u_profile,
            "tweets": user_tweets
        }
        return render(request, "profile.html", context)
    else:
        messages.warning(request, "Log in to view page!")
        return redirect("home")
