import os
import sys

paths = ('/var/www/html/websites/','/var/www/html/websites/toolsprj/')
for path in paths:
    if path not in sys.path:
        sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'toolsprj.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()