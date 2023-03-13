from django.shortcuts import render, redirect
from .models import Profile, Tweet
from django.contrib import messages
from .forms import TweetForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms


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
        return render(request, "home.html", {"tweets": tweets})


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


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You logged in!")
            return redirect("home")
        else:
            messages.warning(request, "No user found! Maybe incorrect username or password")
            return redirect("login")
    return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out")
    redirect("home")


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            first_name = form.cleaned_data["first_name"]
            # last_name = form.cleaned_data["last_name"]
            # email = form.cleaned_data["email"]
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f"{first_name} have registered successfully!")
            return redirect("home")
    return render(request, "register.html", {"form": form})
