from rest_framework import serializers
from api.models import ScreenRecording

class ScreenRecordingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScreenRecording
        fields = ('video_file',)


class ListVideosSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScreenRecording
        fields = '__all__'


class EditFileNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScreenRecording
        field = ('video_title',)

    def update(self, instance, validated_data):
        instance.video_title = validated_data.get('new_filename', instance.video_title)
        instance.save()
        return instance
