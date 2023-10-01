import datetime
import logging
import os
import whisper

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


class VideoUploadAPIView(generics.CreateAPIView):
    serializer_class = ScreenRecordingSerializer
    queryset = ScreenRecording.objects.all()
    parser_classes = (FileUploadParser,)


    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            video_chunks = request.data.get('video_chunks')
            
            combined_data = b''.join([bytes(chunk) for chunk in video_chunks])
            content_file = ContentFile(combined_data)
            filename = content_file.name
            file_path = default_storage.save(filename, content_file)

            # file_path = default_storage.save(filename, ContentFile(file.read()))
            file_url = default_storage.url(file_path)

            instance = ScreenRecording.objects.create(
                video_title=filename, 
                video_file=content_file, 
                video_url=file_url, 
                video_link=reverse('api:play', kwargs={'filename': filename}),
            )
            print(instance.video_url)
            instance.save()

            # url_function(instance.id, instance.video_file, instance.video_link)
            

            return Response({'message': 'Video Upload Complete!'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)
        

class VideoListAPIView(generics.ListAPIView):
    serializer_class = ListVideosSerializer
    queryset = ScreenRecording.objects.all()


@api_view(['GET'])
def video_play_back(request, filename):
    video_path = os.path.join(settings.MEDIA_ROOT, filename)
    print(video_path)
    model = whisper.load_model('base=en')
    options = whisper.DecodingOptions(language='en', fp16=True)
    result = model.transcribe(video_path, options=options)

    save_target = os.path.join(settings.MEDIA_ROOT, 'transcript.vtt')
    
    with open(save_target, 'w') as file:
        for indx, segment in enumerate(result['segments']):
            file.write(str(indx + 1) + '\n')  
            file.write(str(datetime.timedelta(seconds=segment['start'])) + '-->' + str(datetime.timedelta(seconds=segment['end'])) + '\n')
            file.write(segment['text'].strip() + '\n')
            file.write('\n') 

    context = {
        'video': video_path,
        'transcript': save_target
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
    








                