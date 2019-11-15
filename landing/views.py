from django.shortcuts import render, redirect, HttpResponse, reverse
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import RegistrationForm
from my_profile.models import Post, Tag
from landing.models import Friend, ProfileImage, UserProfile


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        else:
            return HttpResponse(
                'You have an error while filling the form ,'
                ' dont forget to set more complex password'
                )
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'accounts/reg_form.html', args)


def view_profile(request, pk=None):
    friends = None
    users = None
    followers = None
    if pk:
        if int(pk) == request.user.id:
            return redirect('accounts:view_profile_with_pk')
        user = User.objects.get(pk=pk)
        user_post = Post.objects.filter(author_id=int(pk)).order_by('-created')
        last_minute = datetime.now(tz=timezone.utc) - timedelta(1)
        results = Post.objects.filter(created__gt=last_minute)
        tags = Tag.objects.all()

    else:
        user = request.user
        user_post = Post.objects.filter(author_id=user.id).order_by('-created')
        last_minute = datetime.now(tz=timezone.utc) - timedelta(1)
        results = Post.objects.filter(created__gt=last_minute).last()
        tags = Tag.objects.all()
        users = User.objects.exclude(id=request.user.id)


        try:
            friend = Friend.objects.get(current_user=request.user)
            friends = friend.users.all()
            followers = friends.count()

        except:
            friends = None
            followers = None


    args = {
        'user': user,
        'post': user_post,
        'post_last': results,
        'tags': tags,
        'friends': friends,
        'users': users,
        'followers': followers,

    }

    return render(request, 'my_profile/home.html', args)


def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if friend:
        if operation == 'add':
            Friend.make_friend(request.user, friend)
            Friend.make_friend(friend, request.user)
        elif operation == 'remove':
            Friend.lose_friend(request.user, friend)
            Friend.lose_friend(friend, request.user)
    return redirect('accounts:view_profile')


def view_friends(request):
    users = User.objects.exclude(id=request.user.id)
    try:
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
    except:
        friends = None
    args = {
    'friends': friends,
    'users': users,
    }
    return render(request, 'accounts/friends.html', args)


def view_profile_friend(request, pk=None):
    friends = None
    users = None
    followers = None
    if pk:
        if int(pk) == request.user.id:
            return redirect('accounts:view_profile_friend')
        user = User.objects.get(pk=pk)
        user_post = Post.objects.filter(author_id=int(pk)).order_by('-created')
        last_minute = datetime.now(tz=timezone.utc) - timedelta(1)
        results = Post.objects.filter(created__gt=last_minute)
        tags = Tag.objects.all()
        users = User.objects.exclude(id=request.user.id)
        try:
            friend = Friend.objects.get(current_user=request.user)
            friends = friend.users.all()
            followers = friends.count()

        except:
            friends = None
            followers = None

    if user.id > request.user.id:
        room_name = f'{user.id}_{request.user.id}'
    else:
        room_name = f'{request.user.id}_{user.id}'
    args = {
        'user': user,
        'post': user_post,
        'post_last': results,
        'tags': tags,
        'friends': friends,
        'users': users,
        'followers': followers,
        'room': reverse('room', kwargs={'room_name': room_name})
    }

    return render(request, 'accounts/friends.html', args)