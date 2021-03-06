
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("profile/<int:user_id>", views.display_profile_view, name="display_profile_view"),
    path("following/", views.following_view, name="following_view"),
    path("create", views.create_post, name="create_post"),
    path("edit", views.edit_post, name="edit_post"),
    path("like", views.like_post, name="like_post"),
    path("follow", views.follow_user, name="follow_user")
]
