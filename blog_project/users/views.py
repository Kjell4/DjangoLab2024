from django.shortcuts import get_object_or_404, render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from .models import Follow, User, Profile
from .forms import ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile_detail', username=user.username)
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def profile_detail(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    
    followers = Follow.objects.filter(following=profile.user)
    following = Follow.objects.filter(follower=profile.user)
    
    followers_list = [follower.follower for follower in followers]
    following_list = [followed.following for followed in following]

    return render(request, 'users/profile.html', {
        'profile': profile,
        'followers_count': followers.count(),
        'following_count': following.count(),
        'followers_list': followers_list,
        'following_list': following_list,
        'is_following': request.user in followers_list,
    })


def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)  
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)  
        if form.is_valid():
            form.save()
            return redirect('profile_detail', username=request.user.username) 
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/edit_profile.html', {'form': form})


def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user != user_to_follow:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('profile_detail', username=username)


def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile_detail', username=username)


