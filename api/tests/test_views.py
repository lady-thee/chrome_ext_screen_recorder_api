from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import ScreenRecording
from api.serializers import ScreenRecordingSerializer

import os


class UploadVideoAPIViewTestcase(APITestCase):
    def setUp(self) -> None:
        video_file_path = os.path.abspath('api/tests/VooTube - Google Chrome 2023-01-15 19-14-32.mp4')
        photo_file_path = os.path.abspath('api/tests/adventuretime.jpg')
        self.data = {
            'video_file': video_file_path,
            'placeholder': photo_file_path
        }
        return self.data 

    def test_upload_view(self):
        url = reverse('api:upload')

        response = self.client.post(url, self.data, format='json')
        print(response)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['message'],'Video Upload Complete!')
        

