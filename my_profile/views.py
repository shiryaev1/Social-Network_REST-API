from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.shortcuts import redirect
from django.contrib import auth
from django.shortcuts import get_object_or_404, HttpResponse
from my_profile.models import *
from landing.forms import EditProfileInformationForm, AddProfileImageForm
from my_profile.forms import TagForm, PostForm
from landing.models import UserProfile


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
        }
        return render(request, self.template_name, args)

    def post(self, request):
        try:
            user = User.objects.get(id=request.user.id)
        except ObjectDoesNotExist:
            return Http404
        form = PostForm(request.POST)
        if form.is_valid():
            form.save(user)
            # return redirect('accounts:view_profile_with_pk')
            form = PostForm()
        args = {
            'user': user,
            'post_form': form,
        }
        return render(request, self.template_name, args)


class PostUpdate(View):
    def get(self,request,slug):
        post = Post.objects.get(slug__iexact=slug)
        bount_form = PostForm(instance=post)
        context = {
            'form': bount_form,
            'post': post
        }
        return render(request,'my_profile/post_update.html', context)

    def post(self,request,slug):
        post = Post.objects.get(slug__iexact=slug)
        bount_form = PostForm(request.POST, request.FILES, instance=post)
        if bount_form.is_valid():
            if 'image' in request.FILES:
                bount_form.image = request.FILES['image']
            new_post = bount_form.save(request.user)
            return redirect('accounts:view_profile')
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
    return render(request, 'my_profile/posts.html', context)


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
    def get(self,request, pk):
        profile = UserProfile.objects.get(pk=pk)
        edit_form = EditProfileInformationForm(instance=profile)
        context = {'form': edit_form, 'profile': profile}
        return render(request, 'accounts/update_edit_profile.html', context)

    def post(self,request, pk):
        profile = UserProfile.objects.get(pk=pk)
        edit_bount_form = EditProfileInformationForm(request.POST or None,
                                                     request.FILES, instance=profile)
        if edit_bount_form.is_valid():
            if 'image' in request.FILES:
                edit_bount_form.image = request.FILES['image']
            edit_bount_form.save(request.user)
            return redirect('accounts:view_profile')
        else:
            print(edit_bount_form.errors)
        context = {'form': edit_bount_form}
        return render(request, 'accounts/update_edit_profile.html', context)


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


