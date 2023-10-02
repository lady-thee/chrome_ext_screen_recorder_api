from django.urls import path
from client.views import list_all_videos, view_video


urlpatterns = [
    path('videos/', list_all_videos, name='videos'),
    path('video/',view_video, name='video'),
]