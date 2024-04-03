from django.urls import path 
from . import views 
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.home, name="home"),
    path("register/",views.register_user, name="register"),
    path("user_profile/<int:pk>", views.user_profile, name="user_profile"),
    path("post/<int:pk>",views.view_post, name="view_post"),
    path("login/",views.login_user, name='login'),
    path("logout/",views.logout_user, name='logout'),
    path("like_post/<int:pk>", views.like_post, name="like_post"),\
    path("user_profile/<int:pk>/update_profile",views.update_profile, name="update_profile"),
    path("follow_user/<int:pk>", views.follow_user, name="follow_user"),
    path("unfollow_user/<int:pk>",views.unfollow_user, name="unfollow_user"),
]