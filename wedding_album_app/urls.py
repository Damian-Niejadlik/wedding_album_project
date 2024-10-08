from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# urlpatterns = [
#     path('', views.album_list, name='album_list'),
#     path('albums/', views.album_list, name='album_list'),
#     path('album/<int:album_id>/', views.album_detail, name='album_detail'),
#     path('album/<int:album_id>/delete/', views.delete_album, name='delete_album'),
#     path('album/<int:album_id>/add_photo/', views.album_detail, name='add_photo'),
#     path('photo/<int:photo_id>/edit/', views.edit_photo, name='edit_photo'),
#     path('photo/<int:photo_id>/delete/', views.delete_photo, name='delete_photo'),
#     path('create_album/', views.create_album, name='create_album'),
#
# ]


# urlpatterns = [
#     path('', views.album_list, name='album_list'),
#     path('albums/', views.album_list, name='album_list'),
#     path('album/<int:album_id>/', views.album_detail, name='album_detail'),
#     path('album/<int:album_id>/delete/', views.delete_album, name='delete_album'),
#     path('album/<int:album_id>/add_photo/', views.album_detail, name='add_photo'),
#     path('photo/<int:photo_id>/edit/', views.edit_photo, name='edit_photo'),
#     path('photo/<int:photo_id>/delete/', views.delete_photo, name='delete_photo'),
#     path('create_album/', views.create_album, name='create_album'),
#     path('album/<int:album_id>/export/pdf/', views.export_album_pdf, name='export_album_pdf'),  # Nowa ścieżka dla PDF
#     path('album/<int:album_id>/export/docx/', views.export_album_docx, name='export_album_docx'),  # Nowa ścieżka dla DOCX
#     path('album/<int:album_id>/export_html/', views.export_album_html, name='export_album_html'),
#
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



urlpatterns = [
    path('', views.album_list, name='album_list'),
    path('albums/', views.album_list, name='album_list'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('album/<int:album_id>/delete/', views.delete_album, name='delete_album'),
    path('album/<int:album_id>/add_photo/', views.album_detail, name='add_photo'),
    path('album/<int:album_id>/capture_photo/', views.capture_photo, name='capture_photo'),  # <-- Dodaj tę ścieżkę
    path('photo/<int:photo_id>/edit/', views.edit_photo, name='edit_photo'),
    path('photo/<int:photo_id>/delete/', views.delete_photo, name='delete_photo'),
    path('create_album/', views.create_album, name='create_album'),
    path('album/<int:album_id>/export/pdf/', views.export_album_pdf, name='export_album_pdf'),
    path('album/<int:album_id>/export/docx/', views.export_album_docx, name='export_album_docx'),
    path('album/<int:album_id>/export/html/', views.export_album_html, name='export_album_html'),
    path('photo/<int:photo_id>/edit/save/', views.save_edited_photo, name='save_edited_photo'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

