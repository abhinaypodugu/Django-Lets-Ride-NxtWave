from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TravelRoute(models.Model):
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travel_routes')
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    travel_medium = models.CharField(max_length=255, choices=[('BUS', 'Bus'), ('CAR', 'Car'), ('TRAIN', 'Train')])
    asset_capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=255, choices=[('APPLIED', 'Applied'), ('NOT_APPLIED', 'Not Applied')], default='NOT_APPLIED')

    def __str__(self):
        return f'{self.pickup_location} to {self.dropoff_location} ({self.start_datetime})'


class AssetTransportationRequest(models.Model):

    requester = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='asset_transportation_request')
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    asset_type = models.CharField(max_length=255, choices=[('LAPTOP', 'Laptop'), ('TRAVEL_BAG', 'Travel Bag'), ('PACKAGE', 'Package')])    
    asset_count = models.PositiveIntegerField()
    sensitivity = models.CharField(max_length=255, choices=[('HIGHLY_SENSITIVE', 'Highly Sensitive'), ('SENSITIVE', 'Sensitive'), ('NORMAL', 'Normal')])
    status = models.CharField(max_length=255, choices=[('Pending', 'Pending'), ('Expired', 'Expired'), ('Completed', 'Completed')], default='Pending')    
    whom_to_deliver = models.CharField(max_length=255)
    rider = models.ForeignKey(User, on_delete=models.CASCADE,related_name='asset_transportation_requests', null=True)
    matched_routes = models.ManyToManyField('TravelRoute', related_name='matched_requests')

    def update_expired_records(self):
        now = timezone.now()
        expired_records = AssetTransportationRequest.objects.filter(start_datetime__lte=now)
        expired_records.update(status='Expired')
