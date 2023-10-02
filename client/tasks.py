from celery import Celery
import whisper
import datetime
from urllib.parse import unquote
from django.conf import settings
import os


app = Celery('config', broker=settings.CELERY_BROKER_URL)
app.config_from_object('django.conf:settings')

@app.task
def transcribe_video(video_path, language='en', fp16=True):
    print(video_path)
    try:
        model = whisper.load_model('base')
        options = whisper.DecodingOptions(language='en', fp16=True)
        result = model.transcribe(video_path)

        print(result)

        vtt_content = ''
        for indx, segment in enumerate(result['segments']):
            vtt_content += (str(indx + 1) + '\n')  
            vtt_content += (str(datetime.timedelta(seconds=segment['start'])) + '-->' + str(datetime.timedelta(seconds=segment['end'])) + '\n')
            vtt_content += (segment['text'].strip() + '\n')
            
        save_target = os.path.join(settings.MEDIA_ROOT, 'transcript')

        with open(save_target, 'w', encoding='utf-8') as file:
            file.write(vtt_content)
            file.write('\n') 

        vvt_url = os.path.join(settings.MEDIA_URL, 'transcript.vtt')
        return vvt_url
    except Exception as e:
        return str