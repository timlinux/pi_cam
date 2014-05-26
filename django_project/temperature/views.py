
import datetime
from django.template.response import TemplateResponse
from models import Temperature


def index(request):
    temperature = Temperature()
    temperature.save()
    return TemplateResponse(
        request,
        'index.html',
        {'temperature': temperature},
        content_type='text/html')
