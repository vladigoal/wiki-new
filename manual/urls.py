from django.conf.urls.defaults import *
from manual.views import *

urlpatterns = patterns('',
    (r'^$', manual_view),
)
