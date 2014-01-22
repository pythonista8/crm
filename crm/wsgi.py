"""
WSGI config for OneKloud CRM project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")

# WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# New Relic
import newrelic.agent

confpath = os.path.join(os.path.dirname(__file__), 'newrelic.ini')
newrelic.agent.initialize(confpath)
application = newrelic.agent.wsgi_application()(application)
