"""lets_ride URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import create_asset_transportation_request, create_travel_route, view_matching_rides, apply_for_ride, view_asset_transportation_requests, IndexPageView, view_travel_routes
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('share_travel_info/', TemplateView.as_view(template_name='main/create_travel_route.html'), name='share_travel_info'),
    path('assets_transport_request/', TemplateView.as_view(
        template_name='main/create_asset_transportation_request.html'), name='assets_transport_request'),
    path('create_asset_transportation_request/', create_asset_transportation_request,
         name='create_asset_transportation_request'),
    path('view_asset_transportation_requests/', view_asset_transportation_requests,
         name='view_asset_transportation_requests'),
    path('create_travel_route/', create_travel_route,
         name='create_travel_route'),
    path('view_matching_rides/<int:request_id>', view_matching_rides,
         name='view_matching_rides'),
    path('apply_for_ride/<int:route_id>/<int:request_id>',
         apply_for_ride, name='apply_for_ride'),
    path('all_travel_routes/', view_travel_routes, name='view_travel_routes'),
]


