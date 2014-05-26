
import datetime
from django.http import HttpResponse

from models import Temperature


def index(request):
    temperature = Temperature()
    temperature.save()
    html = "<html><body>It is now %s.</body></html>" % temperature.temperature
    return HttpResponse(html)
