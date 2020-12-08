import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from .helpers import *


def index(request):
    posts_list = Post.objects.all().order_by('-date_added')
    paginator = Paginator(posts_list, 10) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
    }
    return render(request, "network/index.html", context)
#------------------------------------------------------------------------------------------------------- CREATE POST
@csrf_exempt
@login_required
def create_post(request):

    # CHECKING IF THE METHOD IS POST(REQUIRED TO CREATE POST)
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)
    # REQUEST BODY
    data = json.loads(request.body)

    # GETTING THE DATA AND CHECKING IF IT'S OKAY
    content = data.get("content")
    if len(content) < 10:
        return JsonResponse({
            "error": "You need to write at least 10 characters"
        }, status=400)

    # CREATING THE NEW POST AND SAVING IT
    c_post = Post(
        user=request.user,
        content=content
    )
    c_post.save()
    # RETURNING THE SUCCESS MESSAGE
    return JsonResponse({"message": "Post created successfully."}, status=201)
    #------------------------------------------------------------------------------------------------------- EDIT POST
@login_required
@csrf_exempt
def edit_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("post_id")
        content = data.get("edit_content")
        if len(content) < 10:
            return JsonResponse({
            "error": "You need to write at least 10 characters"
        }, status=400)


        posting = Post.objects.get(pk=post_id)
        posting.content = content
        posting.edited = True
        posting.save()
        return JsonResponse({"message": "Post Saved Successfully"}, status=201)
    return JsonResponse({"error": "Sorry but We need a POST method"}, status=400)
#------------------------------------------------------------------------------------------------------- LIKE/UNLIKE
@login_required
@csrf_exempt
def like_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("id")
        posting = Post.objects.get(pk=post_id)
        user = request.user

        # ADDING OR REMOVING LIKE DEPENDING IF USER IN LIKED LIST
        if user in posting.like.all():
            posting.like.remove(user)
            like_count = posting.like.count()
            liked = False
        else:
            posting.like.add(user)
            like_count = posting.like.count()
            liked = True

        context = {
            "message": "Action completed successfully",
            "likes": like_count,
            "liked": liked,
            "status": 201
        }
        return JsonResponse(context)
    return JsonResponse({}, status= 400)

#------------------------------------------------------------------------------------------------------- FOLLOW/UNFOLLOW USER
@login_required
@csrf_exempt
def follow_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id")
        
        # GETTING THE USERS
        q_user = User.objects.get(pk=user_id)
        current_user = request.user
        # QUERY FOR USERS PROFILES
        q_user_profile = create_profile(q_user)
        current_user_profile = create_profile(current_user)

        # CHECKING WHICH ACTION TO TAKE
        if current_user in q_user_profile.followers.all():
            q_user_profile.followers.remove(current_user)
            current_user_profile.following.remove(q_user)
            followed = False
        else:        
            q_user_profile.followers.add(current_user)
            current_user_profile.following.add(q_user)
            followed = True
        
        
        
        context = {
            "message": "Action completed successfully",
            "followed": followed,
            "followers": q_user_profile.followers.count(),
            "following": q_user_profile.following.count(),
            "status": 201
        }
        return JsonResponse(context)
    return JsonResponse({}, status= 400)
#------------------------------------------------------------------------------------------------------- PROFILE ROUTE
def display_profile_view(request, user_id):
    # GET USERS
    profile_user = User.objects.get(pk=user_id)
    current_user = request.user
    # QUERY FOR PROFILE
    profile = create_profile(profile_user)
    # LOAD THE PROFILE POSTS
    posts_list = profile_user.posts.all().order_by('-date_added')
    # COMPARE IF CURRENT USER IS THE SAME AS THE VIEWED PROFILE
    same_user_check = compare_user(profile_user, current_user)
    # CHECK IF THE CURRENT USER IS FOLLOWING
    if current_user in profile.followers.all():
        following = True
    else:
        following = False
    paginator = Paginator(posts_list, 10) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "profile" : profile,
        "same_user_check": same_user_check,
        "following": following,
    }
    return render(request, "network/profile.html", context)



#------------------------------------------------------------------------------------------------------- FOLLOWING PAGE

def following_view(request):
    current_user = request.user
    users_followed = Profile.objects.get(user=current_user).following.all()    
    posts_list = Post.objects.filter(user__in=users_followed).order_by('-date_added')

    paginator = Paginator(posts_list, 10) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
    }
    return render(request, "network/following.html", context)

#------------------------------------------------------------------------------------------------------- USER LOGIN/REGISTER/LOGOUT
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
