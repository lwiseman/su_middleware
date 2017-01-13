"""
WSGI config for testsessions project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testsessions.settings")

application = get_wsgi_application()

class NGINXMassage(object):
    def __init__(self, application):
        self.application = application
    def __call__(self, environ, start_response):
        environ['REMOTE_USER'] = 'Levi'
        return self.application(environ, start_response)
application = NGINXMassage(application)
