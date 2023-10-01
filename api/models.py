from django.db import models

class ScreenRecording(models.Model):
    """
     The metadata is being stored in order to retrieve the saved videos
    """
    video_title = models.CharField(max_length=252)
    video_file = models.FileField(upload_to='videos/', default='', blank=True)
    # placeholder = models.ImageField(upload_to='screenshots/', default='', blank=True)
    video_link = models.URLField(max_length=200, blank=True)
    video_url = models.URLField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.video_title

