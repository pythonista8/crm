from celery.task.schedules import crontab
from celery.task import periodic_task
from lib.parser import malaysia
from apps.customers.models import SuggestedCompany


@periodic_task
def fetch_companies(run_every=crontab(minute=0, hour=0)):
    list_ = malaysia.fetch()
    for data in list_:
        SuggestedCompany.objects.get_or_create(**data)
