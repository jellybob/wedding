from django.conf.urls.defaults import *

urlpatterns = patterns('wedding.guests.views',
    (r'^$', 'index'),
    (r'^stage2$', 'stage2'),
    (r'^save$', 'save'),
    (r'^confirmed$', 'confirmed'),
)