import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.urls import reverse


from .models import *


def index(request):
    posts = Post.objects.all()
    context = {
        "posts": posts
    }
    return render(request, "network/index.html", context)
#-------------------------------------------------------------------------------------------------------CREATE POST
@csrf_exempt
@login_required
def create_post(request):

    #Creating a new post must be via POST
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)
    #Requests the entire body
    data = json.loads(request.body)

    content = data.get("content", "")
    if len(content) < 10:
        return JsonResponse({
            "error": "You need to write at least 10 characters"
        }, status=400)

    c_post = Post(
        user=request.user,
        content=content
    )
    c_post.save()

    return JsonResponse({"message": "Post created successfully."}, status=201)
#-------------------------------------------------------------------------------------------------------User Profile View
def user_profile_view(request, user_id):
    viewed_user = User.objects.get(pk=user_id)
    posts = viewed_user.posts.all()
    followers = len(Follower.objects.filter(follow=viewed_user))
    following = len(Follower.objects.filter(user=viewed_user))
    follow_check = user_follow_check(request.user, viewed_user)
    context = {
        "viewed_user": viewed_user,
        "posts": posts,
        "followers": followers,
        "following": following,
        "follow_check": follow_check
    }

    return render(request, "network/user_profile.html", context)
#-------------------------------------------------------------------------------------------------------HELPER FUNCTION TO CHECK IF USER IS FOLLOWED OR NOT
def user_follow_check(current_user, viewed_user):
    if len(Follower.objects.filter(user=current_user, follow=viewed_user)) > 0:
        return True
    return False

#------------------------------------------------------------------------------------------------------- FOLLOW/UNFOLLOW ROUTE
def follow(request, user_id):
    follower = Follower()
    viewed_user = User.objects.get(pk=user_id)
    follower.user = request.user
    follower.follow = viewed_user
    follower.save()
    print("USER IS FOLLOWED")
    return redirect(f'/user/{viewed_user.id}')
    

def unfollow(request, user_id):
    viewed_user = User.objects.get(pk=user_id)
    follower = request.user
    Follower.objects.filter(user=follower, follow=viewed_user).delete()
    print("USER IS UNFOLLOWED")
    return redirect(f'/user/{viewed_user.id}')


#-------------------------------------------------------------------------------------------------------USER LOGIN/REGISTER/LOGOUT
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
