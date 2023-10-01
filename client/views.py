from django.shortcuts import render, redirect
from django.urls import reverse



def list_all_videos(request):
    return render(request, 'videos.html')