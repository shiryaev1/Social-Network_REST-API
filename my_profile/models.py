from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time
from django.contrib.auth.models import User


def gen_slug(s):
    new_slug = slugify(s,allow_unicode=True)
    return new_slug + "-" + str(int(time()))


class Post(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    image = models.ImageField(upload_to='post_images/', blank=True)
    content = models.TextField(blank=True, null=True, default=None)
    author = models.ForeignKey(User, blank=True, null=True, default=None,
                               on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag', blank=True, related_name='posts')
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug':self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


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



