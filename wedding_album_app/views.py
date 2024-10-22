import os
from django.shortcuts import render, redirect, get_object_or_404
from wedding_album_project import settings
from .models import Album, Photo
from .forms import AlbumForm, PhotoForm
import base64
from django.core.files.base import ContentFile
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from docx import Document
from reportlab.lib.pagesizes import letter
import io
from docx.shared import Inches
from django.template.loader import render_to_string


def album_list(request):
    albums = Album.objects.all()
    return render(request, 'album_list.html', {'albums': albums})


def create_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('album_list')
    else:
        form = AlbumForm()
    return render(request, 'create_album.html', {'form': form})


def album_detail(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    photos = album.photos.all()

    if request.method == 'POST':
        if 'camera_photo' in request.POST and request.POST['camera_photo']:
            image_data = request.POST['camera_photo']
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image = ContentFile(base64.b64decode(imgstr), name=f'camera_photo.{ext}')
            Photo.objects.create(album=album, image=image)
        else:
            form = PhotoForm(request.POST, request.FILES)
            if form.is_valid():
                photo = form.save(commit=False)
                photo.album = album
                photo.save()
        return redirect('album_detail', album_id=album.id)

    form = PhotoForm()
    return render(request, 'album_detail.html', {'album': album, 'photos': photos, 'form': form})


def delete_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    album.delete()
    return redirect('album_list')


def edit_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    stickers_path = os.path.join(settings.MEDIA_ROOT, 'stickers')
    stickers = [{'image': os.path.join(settings.MEDIA_URL, 'stickers', file)} for file in os.listdir(stickers_path) if
                file.endswith('.png')]

    return render(request, 'edit_photo.html', {'photo': photo, 'stickers': stickers})


def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    album_id = photo.album.id
    photo.delete()
    return redirect('album_detail', album_id=album_id)


def export_album_pdf(request, album_id):
    album = get_object_or_404(Album, id=album_id)

    buffer = io.BytesIO()
    pdf_canvas = canvas.Canvas(buffer, pagesize=letter)

    y = 700
    for photo in album.photos.all():
        if y < 50:
            pdf_canvas.showPage()
            y = 700
        image_path = photo.image.path
        pdf_canvas.drawImage(image_path, 100, y - 100, width=200, height=150)
        y -= 180

    pdf_canvas.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


def export_album_docx(request, album_id):
    album = get_object_or_404(Album, id=album_id)

    document = Document()

    for photo in album.photos.all():
        document.add_picture(photo.image.path, width=Inches(2.0))

    buffer = io.BytesIO()
    document.save(buffer)
    buffer.seek(0)
    response = HttpResponse(buffer,
                            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename={album.title}.docx'
    return response


def export_album_html(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    photos = album.photos.all()

    html_content = render_to_string('album_export.html', {'album': album, 'photos': photos})

    response = HttpResponse(content_type='text/html')
    response['Content-Disposition'] = f'attachment; filename="{album.title}.html"'
    response.write(html_content)

    return response


def add_photo(request, album_id):
    album = get_object_or_404(Album, id=album_id)

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.album = album
            photo.save()
            return redirect('album_detail', album_id=album.id)
    else:
        form = PhotoForm()

    return render(request, 'add_photo.html', {'form': form, 'album': album})


def capture_photo(request, album_id):
    album = get_object_or_404(Album, id=album_id)

    if request.method == 'POST':
        captured_image_data = request.POST.get('captured_image')
        if captured_image_data:
            format, imgstr = captured_image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f'captured_photo.{ext}')

            Photo.objects.create(album=album, image=image_data)
            return redirect('album_detail', album_id=album_id)

    return render(request, 'album_detail.html', {'album': album})


def save_edited_photo(request, photo_id):
    if request.method == 'POST':
        photo = get_object_or_404(Photo, id=photo_id)
        edited_photo_data = request.POST.get('edited_photo_data')

        format, imgstr = edited_photo_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{photo_id}-edited.{ext}')

        photo.image.save(data.name, data)
        return redirect('album_detail', album_id=photo.album.id)
