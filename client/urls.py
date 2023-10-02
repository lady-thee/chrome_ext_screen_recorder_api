from django.urls import path
from client.views import list_all_videos


urlpatterns = [
    path('videos/', list_all_videos, name='videos'),
]