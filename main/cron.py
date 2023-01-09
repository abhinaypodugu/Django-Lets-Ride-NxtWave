from django_crontab import crontab
from .models import AssetTransportationRequest


@crontab(minute='*/2')
def update_expired_records():
    AssetTransportationRequest.update_expired_records()
    print('This is a cron job!')
