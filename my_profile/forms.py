from django import forms
from my_profile.models import Tag, Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['image', 'content']

        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': "What's new?"
                }
            ),
        }

    def save(self, user):
        post = super(PostForm, self).save(commit=False)
        post.author = user
        post.save()



