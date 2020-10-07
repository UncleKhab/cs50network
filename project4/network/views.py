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
        "posts": posts,
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
#-------------------------------------------------------------------------------------------------------Like Route

def like_post(request, post_id):
    posting = Post.objects.get(pk=post_id)
    user = request.user
    posting.like.add(user)
    print('post liked')
    return redirect("index")

def unlike_post(request, post_id):
    posting = Post.objects.get(pk=post_id)
    user = request.user
    posting.like.remove(user)
    print('post unliked')
    return redirect("index")
    
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
