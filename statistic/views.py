from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.http import HttpResponse,StreamingHttpResponse
from django.views.decorators import gzip
from .camera import VideoCamera,VideoCamera1
from .models import Motion
# Motion.objects.all().delete()
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def index(request): 
    return render(request, 
                  'pages/home.html', 
                  {'title': _('Home')})



def statistic(request):
    return render(request, 
                  'pages/statistic.html', 
                  {'data': Motion.objects.all()})

def home(request): 
    return render(request, 
                  'pages/home.html', 
                  {'title': _('Home')})

def video_feed(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")


def video_feed_test(request):
    return HttpResponse(gen(VideoCamera1()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
