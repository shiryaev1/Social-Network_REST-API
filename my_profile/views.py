from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.shortcuts import redirect
from django.contrib import auth

from django.shortcuts import get_object_or_404, HttpResponse
from my_profile.models import *
from landing.forms import EditProfileInformationForm, AddProfileImageForm
from my_profile.forms import PostForm
from landing.models import UserProfile, Friend


def user_photos_view(request):
    return render(request, 'my_profile/edit.html')


class ViewProfile(View):

    template_name = 'my_profile/home.html'

    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)
        except ObjectDoesNotExist:
            raise Http404
        args = {
            'user': user,
            'post_form': PostForm(),
            'posts': Post.objects.filter(author=user).order_by('-id')
        }
        return render(request, self.template_name, args)

    def post(self, request):
        try:
            user = User.objects.get(id=request.user.id)
        except ObjectDoesNotExist:
            return Http404
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            if 'image' in request.FILES:
                form.image = request.FILES['image']
                print(request.FILES['image'])
            # form.image = request.POST['image']
            form.save(user)
            form = PostForm()
        args = {
            'user': user,
            'post_form': form,
            'posts': Post.objects.filter(author=user).order_by('-id')

        }
        return render(request, self.template_name, args)


class PeopleViewProfile(View):

    template_name = 'my_profile/people_page.html'

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404
        if user.id > request.user.id:
            room_name = f'{user.id}_{request.user.id}'
        else:
            room_name = f'{request.user.id}_{user.id}'
        args = {
            'user': user,
            'room': reverse('room', kwargs={'room_name': room_name}),
            'posts': Post.objects.filter(author=user).order_by('-id')
        }
        return render(request, 'my_profile/people_page.html', args)


def click_on_the_contact(request, pk):
    user = User.objects.get(pk=pk)
    if user.id > request.user.id:
        room_name = f'{user.id}_{request.user.id}'
    else:
        room_name = f'{request.user.id}_{user.id}'
    args = {
        'user': user,
        'room': reverse('room', kwargs={'room_name': room_name}),
    }

    return render(request, 'my_profile/test.html', args)


class PostUpdate(View):
    def get(self,request,id):
        post = Post.objects.get(id=id)
        bount_form = PostForm(instance=post)
        context = {
            'form': bount_form,
            'post': post
        }
        return render(request,'my_profile/post_update.html', context)

    def post(self,request,id):
        post = Post.objects.get(id=id)
        bount_form = PostForm(request.POST, request.FILES, instance=post)
        if bount_form.is_valid():
            if 'image' in request.FILES:
                bount_form.image = request.FILES['image']
            new_post = bount_form.save(request.user)
            return redirect('profile')
        else:
            print(bount_form.errors)
        context = {
            'form': bount_form,
            'post': post
        }
        return render(request,'my_profile/post_update.html', context)



class PostDelete(View):
    def get(self,request,slug):
        post_del = Post.objects.get(slug__iexact=slug)
        context = {'post': post_del}
        return render(request,'my_profile/post_delete.html', context)

    def post(self,request,slug):
        post = Post.objects.get(slug__iexact=slug)
        post.delete()
        return redirect('accounts:view_profile')


def posts_list(request):
    posts = Post.objects.all().order_by('-created')
    context = {
        'posts': posts,
        'username': auth.get_user(request).username
    }
    return render(request, 'my_profile/posts_news.html', context)


def profile_information(request, pk=None):
    if pk:
        if int(pk) == request.user.id:
            return redirect('profile_information_url')
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    context = {
        'user': user,
    }
    return render(request, 'accounts/profile_information.html', context)


class EditProfileInformation(View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        profile = UserProfile.objects.get(pk=pk)
        edit_form = EditProfileInformationForm(instance=profile)
        context = {'form': edit_form, 'profile': profile, "user": user}
        return render(request, 'my_profile/edit.html', context)

    def post(self, request, pk):
        profile = UserProfile.objects.get(pk=pk)
        edit_bount_form = EditProfileInformationForm(request.POST or None,
                                                     request.FILES, instance=profile)
        if edit_bount_form.is_valid():
            if 'image' in request.FILES:
                edit_bount_form.image = request.FILES['image']
            edit_bount_form.save(request.user)
            return redirect('profile')
        else:
            print(edit_bount_form.errors)
        context = {'form': edit_bount_form}
        return render(request, 'my_profile/edit.html', context)


class AddProfileImage(View):
    def get(self, request):
        form = AddProfileImageForm()
        return render(request, 'accounts/add_profile_image.html', context={'form': form})

    def post(self, request):
        bount_form = AddProfileImageForm(request.POST, request.FILES)
        if bount_form.is_valid():
            if 'image' in request.FILES:
                bount_form.image = request.FILES['image']
            bount_form.save(request.user)
            return redirect('accounts:view_profile')
        else:
            print(bount_form.errors)
        context = {'form': bount_form}
        return render(request, 'accounts/add_profile_image.html', context)


def add_like(request):
    dislikes = Dislike.objects.filter(post=request.POST.get('post_id'),
                                      user=request.user)
    likes = Like.objects.filter(post=request.POST.get('post_id'),
                                user=request.user)
    post = Post.objects.get(id=request.POST.get('post_id'))

    if not likes:
        if dislikes:
            dislike = Dislike.objects.filter(post=request.POST.get('post_id'),
                                             user=request.user)
            dislike.delete()
            post.dislikes -= 1
        Like.objects.create(post=post, user=request.user)
        post.likes += 1
        post.save()

    return redirect('posts_list_url')


def remove_like(request):
    dislikes = Dislike.objects.filter(post=request.POST.get('post_id'),
                                      user=request.user)
    likes = Like.objects.filter(post=request.POST.get('post_id'),
                                user=request.user)
    post = Post.objects.get(id=request.POST.get('post_id'))
    if not dislikes:
        if likes:
            like = Like.objects.filter(post=request.POST.get('post_id'),
                                       user=request.user)
            like.delete()
            post.likes -= 1
        Dislike.objects.create(post=post, user=request.user)
        post.dislikes += 1
        post.save()

    return redirect('posts_list_url')


def peoples(request):
    users = User.objects.exclude(pk=request.user.pk)
    # friends = Friend.objects.all()
    try:
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
        followers = friends.count()

    except:
        friends = None
        followers = None
    args = {
        "users": users,
        "friends": friends,
    }
    return render(request, 'my_profile/collection.html', args)