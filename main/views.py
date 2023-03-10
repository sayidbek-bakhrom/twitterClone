from django.shortcuts import render, redirect
from .models import Profile
from django.contrib import messages


def home(request):
    return render(request, "home.html")


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, "profile_list.html", {"profiles": profiles})
    else:
        messages.info(request, "Log in to view the page")
        return redirect("home")


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
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

        return render(request, "profile.html", {"profile": profile})
    else:
        messages.warning(request, "Log in to view page!")
        return redirect("home")
