from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    profile_photo = models.ImageField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True) 

    @property 
    def Photourl(self):
        try: 
            url = self.profile_photo.url 
        except:
            url = settings.MEDIA_URL + 'images/default_img.jpg'
        return url 


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Post(models.Model):
    picture = models.ImageField(null=True, blank=True)
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    caption = models.CharField(max_length=100, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    no_of_likes = models.ManyToManyField(CustomUser, related_name="postlikes", blank=True)

    @property 
    def ImageURL(self):
        try:
            url = self.picture.url 
        except:
            url = ''
        return url 


    def __str__(self):
        return f"{self.caption} {self.posted_by}"



class Comment(models.Model):
    commenter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') 
    comment_body = models.CharField(max_length=50, null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.comment} {self.post}"


class Like(models.Model):
    liked_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes') 
    liked_at = models.DateTimeField(auto_now_add=True) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes') 
    

    def __str__(self):
        return f"{self.liked_by} {self.post}"


class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followings')
    created_at = models.DateTimeField(auto_now_add = True) 

    def __str__(self):
        return f"{self.follower}" 
    