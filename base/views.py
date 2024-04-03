from django.shortcuts import render, redirect
from django.contrib import messages 
from .models import *
import json
from django.contrib.auth import login, logout, authenticate 
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .forms import UserRegistrationForm, ProfileUpdateForm


def register_user(request):
    if request.method == 'POST':
        print("success")
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('saved')
            form.save() 
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login') 
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})



def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password'] 

        user = authenticate(request, email=email, password=password) 

        if user is not None:
            login(request, user) 
            messages.success(request, "Logged in successfully") 
            return redirect('home') 
        else:
            messages.error(request, "Invalid credentials") 
            return redirect('home') 
    else:
        return render(request, 'login.html', {}) 

def logout_user(request):
    logout(request) 
    messages.success(request, "Logged out successfully")
    return redirect('home') 


@login_required(login_url=('login/'))
def home(request):
    posts = Post.objects.order_by('-created_at')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password'] 

        user = authenticate(request, username=username, password=password) 
        if user is not None:
            login(request, user) 
            messages.success(request, "Successfully logged in")
            return redirect('home') 
        else:
            messages.error(request, "Invalid credentials") 
            return redirect('home') 
        
    return render(request, "home.html", {'posts':posts}) 

@login_required(login_url=('login/'))
def user_profile(request, pk):
    user = CustomUser.objects.get(id=pk) 
    no_of_followers = Follow.objects.filter(following=pk).count()  
    no_of_following = Follow.objects.filter(follower=pk).count() 
    no_of_posts = Post.objects.filter(posted_by = pk).count() 
    posts = Post.objects.filter(posted_by = pk)

    followers_list = list(Follow.objects.filter(following=user).values_list('follower__email', flat=True))
    followers = Follow.objects.filter(following=user)
    print(followers)
    

    context = {
        'posts':posts,
        'user':user,
        'no_of_followers':no_of_followers,
        'no_of_following':no_of_following,
        'no_of_posts':no_of_posts,
        'followers_list':followers_list,
        'followers':followers,
    }
    
    return render(request, "user_profile.html", context)
    

def like_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=pk)
        if post.no_of_likes.filter(id=request.user.id).exists():
            post.no_of_likes.remove(request.user)
        else:
            post.no_of_likes.add(request.user)
            
    return redirect('view_post', pk=pk)

def view_post(request, pk):
    post = Post.objects.get(id=pk) 
    user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST) 
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post 
            comment.commenter = user 
            comment.save() 
            return redirect('view_post', pk=pk) 
    else:
        form = CommentForm() 
        
    return render(request, 'post.html', {'post':post, 'form':form })

def update_profile(request, pk):
    user = CustomUser.objects.get(id=pk)
    print(user)
    if request.method == 'POST':
        print("success")
        form = ProfileUpdateForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            print('saved')
            form.save() 
            print(user.username)
            messages.success(request, 'Profile Updated.')
            return redirect('user_profile',pk=pk) 
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'update_profile.html', {'form': form,'user':request.user})
    



def follow_user(request, pk):
    # print('hi')
    followed_by = request.user 
    following = CustomUser.objects.get(id=pk) 
    if followed_by != following and not Follow.objects.filter(follower=followed_by, following=following).exists():
        Follow.objects.create(follower = followed_by,following=following)
    return redirect('user_profile',pk=pk)

def unfollow_user(request,pk):
    followed_by = request.user 
    following = CustomUser.objects.get(id=pk) 
    if followed_by!=following and Follow.objects.filter(follower=followed_by, following=following):
        Follow.objects.filter(follower=followed_by, following=following).delete() 
    return redirect('user_profile',pk=pk)