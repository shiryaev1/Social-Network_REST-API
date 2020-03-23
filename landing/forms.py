from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from landing.models import UserProfile, ProfileImage


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditProfileInformationForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['description', 'city', 'website', 'phone', 'sex', 'image',]

        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Write about yourself ..."}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "City"}),
            'website': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Website"}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Phone"}),
            'sex': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Sex"}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'placeholder': "upload image"}),


        }

    def save(self, user):
        user_info = super(EditProfileInformationForm, self).save(commit=False)
        user_info.user = user
        user_info.save()


class AddProfileImageForm(forms.ModelForm):

    class Meta:
        model = ProfileImage
        fields = ['image', 'is_active',]


    def save(self, user):
        user_info = super(AddProfileImageForm, self).save(commit=False)
        user_info.user = user
        user_info.save()




