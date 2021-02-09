from django.urls import path
from .views import index, home,video_feed,video_feed_test,statistic

app_name = 'pages'

urlpatterns = [
    path('', index, name='home'),
    path('home/',home,name='home_function'),
    path('video_feed/',video_feed,name='video_feed'),
    path('video_feed_test/',video_feed_test,name='video_feed_test'),
    path('statistic/',statistic,name='statistic')


]