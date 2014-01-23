"""
Celery settings for Onekloud CRM project.

For more information on this file, see
http://docs.celeryproject.org/en/master/configuration.html
"""

BROKER_HOST = '127.0.0.1'

BROKER_PORT = 5672

BROKER_USER = 'celery'

BROKER_PASSWORD = 'vivendi89'

BROKER_VHOST = 'crm'

CELERY_BACKEND = 'amqp'

CELERY_RESULT_DBURI = ''
