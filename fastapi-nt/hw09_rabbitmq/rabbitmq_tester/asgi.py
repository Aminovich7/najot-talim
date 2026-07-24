"""
ASGI config for rabbitmq_tester project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rabbitmq_tester.settings")

application = get_asgi_application()
