from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    content: models.TextField()
    user: models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post")
    timestamp: models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.id} by {self.user}"
    
class Like(models.Model):
    user: models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    post: models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_like")
    timestamp: models.DateTimeField(auto_now=True)

    def __str__(self) :
        return f"Like {self.id} by {self.user} on post {self.post.id}"
    
class Follow(models.Model):
    user: models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following")
    followed: models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followed")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} follows {self.user}"