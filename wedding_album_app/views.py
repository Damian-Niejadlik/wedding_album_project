import os
from django.shortcuts import render, redirect, get_object_or_404
from wedding_album_project import settings
from .models import Album, Photo
from .forms import AlbumForm, PhotoForm
import base64
from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpResponseForbidden
from reportlab.pdfgen import canvas
from docx import Document
from reportlab.lib.pagesizes import letter
import io
from docx.shared import Inches
from django.template.loader import render_to_string

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


@login_required
def album_list(request, username):
    if username != request.user.username:
        return redirect('album_list', username=request.user.username)

    albums = Album.objects.filter(user=request.user)
    return render(request, 'album_list.html', {
        'albums': albums,
        'username': request.user.username,
        'profile': request.user,
    })


@login_required
def create_album(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        form = AlbumForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            return redirect('album_list', username=username)
    else:
        form = AlbumForm(user=user)

    return render(request, 'create_album.html', {'form': form})


@login_required
def album_detail(request, username, album_id):
    user = get_object_or_404(User, username=username)
    album = get_object_or_404(Album, id=album_id, user=user)

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = user
            photo.album = album
            photo.save()
            return redirect('album_detail', username=username, album_id=album_id)
    else:
        form = PhotoForm()

    photos = album.photos.all()
    return render(request, 'album_detail.html', {'album': album, 'photos': photos, 'form': form})


@login_required
def delete_album(request, album_id):
    album = get_object_or_404(Album, id=album_id, user=request.user)
    if request.method == "POST":
        album.delete()
        return redirect('album_list', username=request.user.username)
    return HttpResponseForbidden()


@login_required
def add_photo(request, username, album_id):
    user = get_object_or_404(User, username=username)
    album = get_object_or_404(Album, id=album_id, user=user)

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = user
            photo.album = album
            photo.save()
            return redirect('album_detail', username=username, album_id=album_id)
    else:
        form = PhotoForm()

    return render(request, 'add_photo.html', {'form': form, 'album': album})


@login_required
def edit_photo(request, username, photo_id):
    user = get_object_or_404(User, username=username)
    photo = get_object_or_404(Photo, id=photo_id, user=user)

    stickers_path = os.path.join(settings.MEDIA_ROOT, 'stickers')
    stickers = [{'image': os.path.join(settings.MEDIA_URL, 'stickers', file)} for file in os.listdir(stickers_path) if
                file.endswith('.png')]

    return render(request, 'edit_photo.html', {'photo': photo, 'stickers': stickers})


@login_required
def delete_photo(request, username, photo_id):
    if request.user.username != username:
        return redirect('login')
    photo = get_object_or_404(Photo, id=photo_id, user=request.user)
    album_id = photo.album.id
    photo.delete()
    return redirect('album_detail', username=username, album_id=album_id)


@login_required
def capture_photo(request, username, album_id):
    if request.method == 'POST':
        captured_image = request.POST.get('captured_image')
        if captured_image:
            print("Otrzymano zdjęcie:", captured_image[:100])
            format, imgstr = captured_image.split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f"photo.{ext}")

            user = get_object_or_404(User, username=username)
            album = get_object_or_404(Album, id=album_id, user__username=user)
            photo = Photo.objects.create(album=album, image=image_data, user=user)
            photo.user = user
            photo.album = album
            photo.save()

            messages.success(request, "Zdjęcie zostało dodane.")
            return redirect('album_detail', username=username, album_id=album.id)
    messages.error(request, "Nie udało się zapisać zdjęcia.")
    return redirect('album_detail', username=username, album_id=album_id)


@login_required
def export_album_pdf(request, username, album_id):
    album = get_object_or_404(Album, id=album_id, user=request.user)

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


@login_required
def export_album_docx(request, username, album_id):
    album = get_object_or_404(Album, id=album_id, user=request.user)

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


@login_required
def export_album_html(request, username, album_id):
    album = get_object_or_404(Album, id=album_id, user=request.user)
    photos = album.photos.all()
    full_path = settings.MEDIA_ROOT

    html_content = render_to_string('album_export.html', {'album': album, 'photos': photos, "full_path": full_path})

    response = HttpResponse(content_type='text/html')
    response['Content-Disposition'] = f'attachment; filename="{album.title}.html"'
    response.write(html_content)

    return response


@login_required
def save_edited_photo(request, username, photo_id):
    if request.user.username != username:
        return redirect('login')
    photo = get_object_or_404(Photo, id=photo_id, user=request.user)
    if request.method == 'POST':
        edited_photo_data = request.POST.get('edited_photo_data')
        format, imgstr = edited_photo_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{photo_id}-edited.{ext}')

        photo.image.save(data.name, data)
        return redirect('album_detail', username=username, album_id=photo.album.id)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        confirm_email = request.POST.get('confirm_email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Walidacja pól
        if email != confirm_email:
            messages.error(request, "Adresy e-mail nie pasują.")
            return redirect('register')
        if password != confirm_password:
            messages.error(request, "Hasła nie pasują.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ta nazwa użytkownika jest zajęta.")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Ten adres e-mail jest już zarejestrowany.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        login(request, user)
        return redirect(f'/{username}/')

    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Witaj, {username}!")
                return redirect('album_list', username=user.username)
            else:
                messages.error(request, "Nieprawidłowy login lub hasło.")
        else:
            messages.error(request, "Nieprawidłowy login lub hasło.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def home(request):
    return render(request, 'home.html')


def user_logout(request):
    logout(request)
    messages.success(request, "Zostałeś wylogowany.")
    return redirect('/')
