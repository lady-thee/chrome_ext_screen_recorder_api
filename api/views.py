import datetime
import logging
import os
import uuid
import whisper
import datetime
import logging
import os
from api.tasks import transcribe_video

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from api.models import ScreenRecording
from api.serializers import ScreenRecordingSerializer, ListVideosSerializer, EditFileNameSerializer
import ffmpeg 

class VideoUploadAPIView(generics.CreateAPIView):
    serializer_class = ScreenRecordingSerializer
    queryset = ScreenRecording.objects.all()
    parser_classes = (FileUploadParser,)
    http_method_names = ['post']


    def create(self, request, *args, **kwargs):
        try:
            video_data = request.body  # Get the binary video data from the request body
            filename = 'recording.mp4'

            # Validate binary data (example: check for minimum size)
            if len(video_data) < 100:
                return Response({'error': 'Invalid binary data'}, status=status.HTTP_400_BAD_REQUEST)


            unique_filename = str(uuid.uuid4()) + '_recording.mp4'

            instance = ScreenRecording.objects.create(
                video_title=filename,
                video_file=ContentFile(video_data, name=filename),
                # video_url=file_url,
                video_link=reverse('api:play', kwargs={'filename': filename}),
            )
            print(instance)
            # print(instance.video_file)
            instance.save()

            # Convert the binary data to a playable video format (e.g., MP4) using MoviePy
            try:
                 # Convert the binary data to a playable video format (e.g., MP4) using FFmpeg
                 # Convert the binary data to a playable video format (e.g., MP4) using FFmpeg
                input_filename = instance.video_file.path
                output_filename = instance.video_file.path.replace('.mp4', '_converted.webm')

                # Use FFmpeg to perform the conversion
                (
                    ffmpeg.input(input_filename)
                    .output(output_filename, vcodec='libvpx', acodec='copy')
                    .run()
                )

                # Update the instance with the converted video file
                instance.video_file = ContentFile(open(output_filename, 'rb').read(), name=unique_filename)
                instance.save()

                return Response({'message': 'Video Upload Complete!'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)})
        except Exception as e:
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)
        



class VideoListAPIView(generics.ListAPIView):
    serializer_class = ListVideosSerializer
    queryset = ScreenRecording.objects.all()


@api_view(['GET'])
def video_play_back(request, filename):
    video_path = os.path.join(settings.MEDIA_ROOT, filename)
    print(video_path)
    
    vtt_url = transcribe_video(video_path)
    context ={
        'video': video_path,
        'transcript': vtt_url
    }

    return render(request, 'videoplay.html', context)


class EditFilenameAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = EditFileNameSerializer
    queryset = ScreenRecording.objects.all()

    def get_object(self):
        pk = self.kwargs.get('pk')
        return self.queryset.get(id=pk)

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Filename Updated Successfully!'}, status=status.HTTP_202_ACCEPTED)
    








                