from django.conf.urls.defaults import *

urlpatterns = patterns('wedding.guests.views',
    (r'^$', 'index'),
    (r'^save$', 'save'),
    (r'^confirmed$', 'confirmed'),
)