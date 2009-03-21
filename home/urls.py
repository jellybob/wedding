from django.conf.urls.defaults import *

urlpatterns = patterns('wedding.home.views',
    (r'^$', 'index'),
)