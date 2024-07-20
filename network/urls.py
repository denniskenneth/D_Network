
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>/", views.profile, name="profile"),
    path("<str:page_name>/posts", views.posts_route, name="posts_route"),

    # API
    path("follow/<int:user_id>/", views.follow, name="follow"),
    path("posts/<str:page_name>/", views.posts, name="posts"),
    path("toggle_like/<int:post_id>/", views.toggle_Like, name="toggle_like"),
]
