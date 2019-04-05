from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','image']

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ['title']

    class Meta:
        model = Tag


admin.site.register(Tag, TagAdmin)


class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']

    class Meta:
        model = Like


admin.site.register(Like, LikeAdmin)


class DislikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']

    class Meta:
        model = Dislike


admin.site.register(Dislike, DislikeAdmin)


