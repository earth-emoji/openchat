from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.db import transaction
from django.forms.utils import ValidationError

from accounts.models import UserProfile
from photos.models import Album, Photo
from users.models import User


class UserSignUpForm(UserCreationForm):
    username = forms.CharField(min_length=1, max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(min_length=1, max_length=60, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    name = forms.CharField(min_length=1, max_length=60, widget=forms.TextInput(attrs={'class': 'form-control'}))
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    password1 = forms.CharField(min_length=1, max_length=60, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(min_length=1, max_length=60, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'name', 'email', 'photo')

    @transaction.atomic
    def save(self):
        user = super().save()
        profile = UserProfile.objects.create(user=user)
        album = Album.objects.create(name=user.username, owner=profile)
        Photo.objects.create(url=self.cleaned_data.get('photo'), album=album, default=True)
        profile.albums.add(album)
        return user
