from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import auth
from django.shortcuts import get_object_or_404
from my_profile.models import *
from landing.forms import EditProfileInformationForm
from my_profile.forms import TagForm, PostForm


class PostCreate(View):
    def get(self,request):
        form = PostForm()
        return render(request,'my_profile/post_create.html',context={'form':form})

    def post(self,request):
        bount_form = PostForm(request.POST)
        if bount_form.is_valid():
            new_post = bount_form.save(request.user)
            return redirect('accounts:view_profile')
        context = {'form': bount_form}
        return render(request,'my_profile/post_create.html', context)


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
        bount_form = PostForm(request.POST,instance=post)
        if bount_form.is_valid():
            new_post = bount_form.save(request.user)
            return redirect('accounts:view_profile')
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
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'username': auth.get_user(request).username
    }
    return render(request, 'my_profile/posts.html', context)


class TagDetail(View):
    def get(self,request,slug):
        tag = get_object_or_404(Tag,slug__iexact=slug)
        context = {'tag': tag}
        return render(request,'my_profile/tag_detail.html', context)


class TagCreate(View):
    def get(self,request):
        form = TagForm()
        context = {'form': form}
        return render(request,'my_profile/tag_create.html', context)

    def post(self,request):
        bount_form = TagForm(request.POST)
        if bount_form.is_valid():
            new_tag = bount_form.save()
            return redirect(new_tag)
        context = {'form': bount_form}
        return render(request,'my_profile/tag_create.html', context)


class TagUpdate(View):
    def get(self,request,slug):
        tag = Tag.objects.get(slug__iexact=slug)
        bount_form = TagForm(instance=tag)
        context = {
            'form': bount_form,
            'tag': tag
        }

        return render(request, 'my_profile/tag_update_form.html', context)

    def post(self,request,slug):
        tag = Tag.objects.get(slug__iexact=slug)
        bount_form = TagForm(request.POST,instance=tag)
        if bount_form.is_valid():
            new_form = bount_form.save()
            return redirect(new_form)
        context = {
            'form': bount_form,
            'tag': tag
        }
        return render(request,'my_profile/tag_update_form.html', context)


def tags_list(request):
    tags = Tag.objects.all()
    context = {'tags': tags}
    return render(request,'my_profile/tags_list.html',context)


def profile_information(request,pk=None):
    if pk:
        if int(pk) == request.user.id:
            return redirect('profile_information_url')
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    context = {'user': user}
    return render(request,'accounts/profile_information.html', context)


class EditProfileInformation(View):
    def get(self,request):
        edit_form = EditProfileInformationForm()
        context = {'form': edit_form}
        return render(request, 'accounts/edit_profile.html', context)

    def post(self,request):
        edit_bount_form = EditProfileInformationForm(request.POST or None)
        if edit_bount_form.is_valid():
            new_post = edit_bount_form.save(request.user)
            return redirect('profile_information_url')
        context = {'form': edit_bount_form}
        return render(request, 'accounts/edit_profile.html', context)


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