"""
WSGI config for BestProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BestProject.settings')

vercel_env = os.environ.get('VERCEL_ENV', None)

if vercel_env == 'true':
    app = get_wsgi_application()
else:
    application = get_wsgi_application()