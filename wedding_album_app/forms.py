from django import forms
from .models import Album, Photo


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title']


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
