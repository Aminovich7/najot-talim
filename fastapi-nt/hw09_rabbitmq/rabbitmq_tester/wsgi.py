"""
WSGI config for rabbitmq_tester project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rabbitmq_tester.settings")

application = get_wsgi_application()
