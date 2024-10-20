from django.db import models


class Album(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Photo(models.Model):
    album = models.ForeignKey(Album, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Zdjęcie w albumie {self.album.title}"


class Sticker(models.Model):
    image = models.ForeignKey(Photo, related_name='stickers', on_delete=models.CASCADE)
    sticker = models.ImageField()

    def __str__(self):
        return f"Nakleja {self.image.title}"