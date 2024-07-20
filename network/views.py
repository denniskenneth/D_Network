from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import json


from .models import User, Post, Follow, Like

def paginator(posts, page):
     paginator = Paginator(posts, 10)
     page_posts = paginator.get_page(page)
     return page_posts
    
def index(request):
    if request.method == "POST":
        content = request.POST["content"]
        print(content)
        post = Post(content=content, user=request.user, timestamp=timezone.now())
        print(post)
        post.save()
        return redirect("index")
    elif request.method == "PUT":

        try:
            data = json.loads(request.body)

            post_id = data.get("post_id")
            content = data.get("content")
            post = Post.objects.get(pk=post_id,)
            post.content = content
            post.save()
            print (post.content);
            return JsonResponse({"status": "success", "data": post.content}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Post not found."}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    


    posts = Post.objects.all().order_by("-timestamp")

    # Pagination
    page = request.GET.get("page")
    page_posts = paginator(posts,page)
    
    # page_posts = paginator.get_page(page)
    # print(page_posts)
    return render(request, "network/index.html", {
        # "posts": posts,
        "page_posts": page_posts,
        })




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
    

@login_required
def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    is_profile = request.user == user
    is_following = Follow.objects.filter(user=request.user, followed=user).exists()
    following_count = user.user_following.count()
    followers_count = user.user_followed.count()
    posts = user.user_post.all().order_by('-timestamp')

    # Pagination
    page = request.GET.get("page")
    page_posts = paginator(posts,page)

    return render(request, "network/profile.html", {
        "user1":user,
        # "posts": posts,
        "is_profile": is_profile,
        "following_count": following_count,
        "follower_count": followers_count,
        "is_following": is_following,
        "page_posts": page_posts,
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


def posts_route(request, page_name):
    if page_name == 'all' or page_name == "following":
        
        postss = posts(request, page_name)

        # Pagination
        page = request.GET.get("page")
        page_posts = paginator(postss,page)

        return render(request, "network/posts.html", {
                "page_posts": postss,
                "page_name": page_name.capitalize(),
                "page_posts": page_posts,
            }
            )

    return render(request, "network/error.html")



def posts(request, page_name):
        posts = []
    # try:
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

       
        return posts
   

def toggle_Like(request, post_id):
    if request.method == "POST":
        try:
            post = get_object_or_404(Post, pk=post_id)
            user = request.user

            # Check if the user has already liked the post
            liked = Like.objects.filter(user=user, post=post).exists()

            if liked:
                # unlike the post
                Like.objects.filter(user=user, post=post).delete()
                liked = False
            else:
                # Like the post
                Like.objects.create(user=user, post=post)
                liked = True

            # Get the updated like count
            like_count = post.post_like.count()

            return JsonResponse({"liked": liked, "like_count":like_count})

        except Post.DoesNotExist:
            return JsonResponse({"error": "Post does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)


    return JsonResponse({"error": "Invalid request method."}, status=405)  # Method Not Allowed