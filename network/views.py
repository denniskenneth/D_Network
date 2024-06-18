from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Post, Follow


def index(request):
    if request.method == "POST":
        content = request.POST["content"]
        print(content)
        post = Post(content=content, user=request.user, timestamp=timezone.now())
        print(post)
        post.save()
        return redirect("index")
    
 
    posts = Post.objects.all().order_by("-timestamp")
    print(posts)
    return render(request, "network/index.html", {"posts": posts})




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
    


def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    is_profile = request.user == user
    is_following = Follow.objects.filter(user=request.user, followed=user).exists()
    following_count = user.user_following.count()
    followers_count = user.user_followed.count()
    posts = user.user_post.all().order_by('-timestamp')
    return render(request, "network/profile.html", {
        "user1":user,
        "posts": posts,
        "is_profile": is_profile,
        "following_count": following_count,
        "follower_count": followers_count,
        "is_following": is_following,
    })

def follow(request, user_id):
    if request.method == "POST":
        
        try:
            user = get_object_or_404(User, pk=user_id)
            # Attempt to create a follow relationship
            follow, created = Follow.objects.get_or_create(user=request.user, followed=user)
            if created:
                # The follow relationship was successfully created
                message = "You are now following this user."
                status = 201  # Created
            else:
                # The follow relationship already exists

                follow.delete()
                message = "You are already following this user."
                status = 200  # OK

            return JsonResponse({"message": message}, status=status)
       
        except User.DoesNotExist:
                return JsonResponse({"error": "User does not exist."}, status=404)
            
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)  # Method Not Allowed


def posts(request, page_name):
    try:
        # Check if the request is for all posts
        if page_name == "all":
            # Retrieve all posts ordered by timestamp in descending order
            posts = Post.objects.all().order_by("-timestamp")
        else:
            # Retrieve posts for a specific user
            # Get the list of users the current user is following
            following_users = request.user.user_following.all().values_list('followed', flat=True)
            
            # Filter posts to include only those from the followed users
            posts = Post.objects.filter(user__in=following_users).order_by("-timestamp")

        # Serialize the posts data
        posts_data = [
            {
                "id": post.id,
                "content": post.content,
                "user": post.user.username,
                "timestamp": post.timestamp,
            }
            for post in posts
        ]

        # Return the serialized data as JSON with a 200 status code
        return JsonResponse(posts_data, safe=False, status=200)

    except ObjectDoesNotExist:
        # Handle the case where the user does not exist
        return JsonResponse({"error": "User not found"}, status=404)

    except Exception as e:
        # Handle any other exceptions
        return JsonResponse({"error": str(e)}, status=500)