from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .api_views import AlbumListCreateAPIView, AlbumDetailAPIView, PhotoListCreateAPIView, PhotoDetailAPIView

from .views import home

urlpatterns = [
                  path('', home, name='home'),
                  path('login/', views.user_login, name='login'),
                  path('logout/', views.user_logout, name='logout'),
                  path('register/', views.register, name='register'),
                  path('<str:username>/', views.album_list, name='album_list'),
                  path('<str:username>/albums/', views.album_list, name='album_list'),
                  path('<str:username>/create_album/', views.create_album, name='create_album'),
                  path('<str:username>/album/<int:album_id>/', views.album_detail, name='album_detail'),
                  path('<str:username>/album/<int:album_id>/delete/', views.delete_album, name='delete_album'),
                  path('<str:username>/album/<int:album_id>/add_photo/', views.album_detail, name='add_photo'),
                  path('<str:username>/album/<int:album_id>/capture_photo/', views.capture_photo, name='capture_photo'),
                  path('<str:username>/photo/<int:photo_id>/edit/', views.edit_photo, name='edit_photo'),
                  path('<str:username>/photo/<int:photo_id>/delete/', views.delete_photo, name='delete_photo'),
                  path('<str:username>/album/<int:album_id>/export/pdf/', views.export_album_pdf,
                       name='export_album_pdf'),
                  path('<str:username>/album/<int:album_id>/export/docx/', views.export_album_docx,
                       name='export_album_docx'),
                  path('<str:username>/album/<int:album_id>/export/html/', views.export_album_html,
                       name='export_album_html'),
                  path('<str:username>/photo/<int:photo_id>/edit/save/', views.save_edited_photo,
                       name='save_edited_photo'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('api/albums/', AlbumListCreateAPIView.as_view(), name='api_album_list_create'),
    path('api/albums/<int:pk>/', AlbumDetailAPIView.as_view(), name='api_album_detail'),
    path('api/photos/', PhotoListCreateAPIView.as_view(), name='api_photo_list_create'),
    path('api/photos/<int:pk>/', PhotoDetailAPIView.as_view(), name='api_photo_detail'),
]
