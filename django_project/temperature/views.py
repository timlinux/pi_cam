import subprocess
import datetime
from core.settings import MEDIA_ROOT
from django.template.response import TemplateResponse
from models import Temperature


def index(request):
    temperature = Temperature()
    temperature.save()
    time = datetime.now()
    filename = 'MEDIA_ROOT/cam-%04d%02d%02d-%02d%02d%02d.jpg' % (
        MEDIA_ROOT, time.year, time.month, time.day, time.hour, time.minute, time.second)
    quality = 15
    subprocess.call("raspistill %s -w %s -h %s -t 200 -e jpg -q %s -n -o %s" % (
        '-br 30 -rot 270', 800, 600, quality, filename), shell=True)
    return TemplateResponse(
        request,
        'index.html',
        {
            'temperature': temperature,
            'filename': filename
        },
        content_type='text/html')
