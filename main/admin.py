from django.contrib import admin

from .models import AssetTransportationRequest, TravelRoute

# Register your models here.
admin.site.register(TravelRoute)
admin.site.register(AssetTransportationRequest)
