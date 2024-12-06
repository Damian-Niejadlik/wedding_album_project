from django.db import models
from django.contrib.auth.models import User


class Album(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="albums")

    def __str__(self):
        return self.title


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Sticker(models.Model):
    image = models.ForeignKey(Photo, related_name='stickers', on_delete=models.CASCADE)
    sticker = models.ImageField()

    def __str__(self):
        return f"Nakleja {self.image.title}"
