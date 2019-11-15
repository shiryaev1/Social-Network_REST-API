from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time
from django.contrib.auth.models import User


class Post(models.Model):
    image = models.ImageField(upload_to='post_images/', blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, blank=True, null=True, default=None,
                               on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)

    def get_create_url(self):
        return reverse('post_create_url', kwargs={'id':self.id})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'id': self.id})

    def __str__(self):
        return str(self.content)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def __str__(self):
        return "Тег %s " % self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Тэги'



