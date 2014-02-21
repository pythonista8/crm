from celery.task import periodic_task
from celery.task.schedules import crontab
from lib.parser import malaysia
from apps.customers.models import SuggestedCompany


@periodic_task(run_every=crontab(minute=0, hour=0))
def fetch_companies():
    list_ = malaysia.fetch()
    for data in list_:
        company, created = SuggestedCompany.objects.get_or_create(**data)
        print(company, created)
