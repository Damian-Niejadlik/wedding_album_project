from django import forms
from .models import Album, Photo
from django.contrib.auth.models import User


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        album = super().save(commit=False)
        if self.user:
            album.user = self.user
        if commit:
            album.save()
        return album


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.album = kwargs.pop('album', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        photo = super().save(commit=False)
        if self.user:
            photo.user = self.user
        if self.album:
            photo.album = self.album
        if commit:
            photo.save()
        return photo


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
