from django.conf.urls.defaults import *

urlpatterns = patterns('wedding.gifts.views',
    (r'^$', 'index'),
    (r'^reserve$', 'reserve')
)