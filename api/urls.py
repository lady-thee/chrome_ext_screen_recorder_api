from django.conf import settings
from django.urls import path 
from django.views.static import serve
from api.views import (video_play_back,
                        EditFilenameAPIView, 
                        VideoUploadAPIView, 
                        VideoListAPIView)

app_name = 'api'

urlpatterns = [
    # path('serve/<str:video_filename>/', serve, {'document_root': settings.MEDIA_ROOT} ,name='video_serve'),
    path('upload/', VideoUploadAPIView.as_view(), name='upload'),
    path('recordings/', VideoListAPIView.as_view(), name='recordings'),
    # path('recording/<str:pk>/', VideoDownloadAPIView.as_view(), name='recording'),
    path('play/<str:filename>/', video_play_back, name='play'),
    path('edit/<str:pk>/', EditFilenameAPIView.as_view(), name='edit')
]