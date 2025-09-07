"""
ASGI config for phone_book project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from phone_book.configurations import DEBUG

from django.core.asgi import get_asgi_application

if DEBUG:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phone_book.phone_book.settings.dev_settings")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phone_book.phone_book.settings.prod_settings")

application = get_asgi_application()
