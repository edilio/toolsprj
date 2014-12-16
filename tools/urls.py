__author__ = 'edilio'

from django.conf.urls.defaults import *
from tools import views

urlpatterns = patterns('',
    # Example:

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    url(r'^$', views.home, name='tools_home'),
    url(r'^(?P<tool_id>\d+)/$', views.run_tool, name='run_tool'),
    url(r'^center-text-image$', views.center_text_image, name='center-text-image'),
    url(r'^create-image$', views.create_image_view, name='create-image'),


)
