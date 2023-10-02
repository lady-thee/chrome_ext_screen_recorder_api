from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
import datetime
import logging
import os
import whisper
from client.tasks import transcribe_video


def list_all_videos(request):
    return render(request, 'videos.html')

from urllib.parse import unquote

def view_video(request):
    decoded = unquote('2023-02-20 22-01-50.mkv')
    video_path = os.path.join(settings.MEDIA_ROOT, decoded)
    print(video_path)
    
    vtt_url = transcribe_video.delay(video_path).get()
    context ={
        'video': video_path,
        'transcript': vtt_url
    }
    return render(request, 'videoplay.html', context)