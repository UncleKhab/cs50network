
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("like/<int:post_id>", views.like_post, name="like_post"),
    path("unlike/<int:post_id>", views.unlike_post, name="unlike_post"),

    # API Routes
    path("create", views.create_post, name="create_post"),
]
