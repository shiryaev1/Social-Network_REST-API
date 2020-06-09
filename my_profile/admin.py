from django.contrib import admin
from .models import *


admin.site.register(Post)


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
admin.site.register(ProfileFile)