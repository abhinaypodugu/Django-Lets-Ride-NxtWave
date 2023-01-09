from django.db.models import Q
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from .models import AssetTransportationRequest, TravelRoute
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, EmptyPage

class IndexPageView(TemplateView):
    template_name = 'main/index.html'

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------


@login_required
def view_travel_routes(request):

    # view function for displaying all available travel routes
    # get the current page number from the request query parameters
    page_number = request.GET.get('page', 1)

    # create a paginator object with 10 routes per page
    paginator = Paginator(TravelRoute.objects.all(), 10)

    try:
        # retrieve the current page of routes
        routes = paginator.page(page_number)
    except PageNotAnInteger:
        # if the page number is not an integer, show the first page
        routes = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, show the last page
        routes = paginator.page(paginator.num_pages)

    return render(request, 'main/view_travel_routes.html', {'routes': routes, 'page': routes})

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------


@login_required
def view_asset_transportation_requests(request):
    # get the request parameters
    sort = request.GET.get('sort')
    status = request.GET.get('status')
    asset_type = request.GET.get('asset_type')
    page = request.GET.get('page')

    # create the queryset for the requests
    requests = AssetTransportationRequest.objects.filter(
        requester=request.user)
    if status:
        requests = requests.filter(status=status)
    if asset_type:
        requests = requests.filter(asset_type=asset_type)

    # sort the queryset
    if sort == 'asc':
        requests = requests.order_by('start_datetime')
    elif sort == 'desc':
        requests = requests.order_by('-start_datetime')

    # paginate the queryset
    paginator = Paginator(requests, 10)
    requests = paginator.get_page(page)

    # build the response data
    data = {
        'requests': [{
            'id': request.id,
            'pickup_location': request.pickup_location,
            'dropoff_location': request.dropoff_location,
            'asset_type': request.asset_type,
            'asset_count': request.asset_count,
            'start_datetime': request.start_datetime,
            'sensitivity': request.sensitivity,
            'rider': request.rider,
            'whom_to_deliver': request.whom_to_deliver,
            'status': request.status,
        } for request in requests],
        'page': requests,
        'status': status,
        'asset_type': asset_type,
        'sort': sort,
    }
    return render(request, 'main/view_asset_transportation_requests.html', context=data)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------


@login_required
def view_matching_rides(request, request_id):
    asset_request = AssetTransportationRequest.objects.get(id=request_id)
    matching_rides = TravelRoute.objects.filter(
        pickup_location=asset_request.pickup_location,
        dropoff_location=asset_request.dropoff_location,
        start_datetime__gt=asset_request.start_datetime,
        status='NOT_APPLIED'
    ).exclude(rider=request.user)
    paginator = Paginator(matching_rides, 10)
    matching_rides_page = paginator.get_page(1)
    data = [{
        'id': ride.id,
        'pickup_location': ride.pickup_location, 
        'dropoff_location': ride.dropoff_location,
        'start_datetime': ride.start_datetime,
        'travel_medium': ride.travel_medium, 
        'no_of_assets': ride.asset_capacity, 
        'status': ride.status,
        'rider': ride.rider
        }
            for ride in matching_rides_page]
    # render the template
    return render(request, 'main/view_matching_rides.html', {'matching_rides': data, 'request_id': request_id})

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------


@login_required
def apply_for_ride(request, route_id, request_id):
    ride = TravelRoute.objects.get(id=route_id)
    asset_request = AssetTransportationRequest.objects.get(id=request_id)
    ride.status = 'APPLIED'
    asset_request.rider = request.user
    asset_request.status = 'Completed'
    ride.save()
    asset_request.save()
    return JsonResponse({'status': 'success'})

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------


@login_required
def create_asset_transportation_request(request):
    if request.method == 'POST':
        # get the request data
        data = request.POST
        pickup_location = data.get('pickup_location')
        dropoff_location = data.get('dropoff_location')
        asset_type = data.get('asset_type')
        asset_count = data.get('asset_count')
        sensitivity = data.get('sensitivity')
        start_datetime = data.get('start_datetime')
        whom_to_deliver = data.get('whom_to_deliver')

        # validate the input data
        if asset_type not in ['LAPTOP', 'TRAVEL_BAG', 'PACKAGE']:
            return JsonResponse({'error': 'Invalid asset type'}, status=400)
        if sensitivity not in ['HIGHLY_SENSITIVE', 'SENSITIVE', 'NORMAL']:
            return JsonResponse({'error': 'Invalid sensitivity level'}, status=400)
        if not pickup_location or not dropoff_location:
            return JsonResponse({'error': 'Pickup and dropoff locations are required'}, status=400)

        # create the asset transportation request
        request = AssetTransportationRequest.objects.create(
            requester=request.user,
            pickup_location=pickup_location,
            dropoff_location=dropoff_location,
            asset_type=asset_type,
            asset_count=asset_count,
            sensitivity=sensitivity,
            start_datetime=start_datetime,
            whom_to_deliver=whom_to_deliver
        )
        return redirect(f'/view_matching_rides/{request.id}')
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------


@login_required
def create_travel_route(request):
    if request.method == 'POST':
        # get the request data
        data = request.POST
        pickup_location = data.get('pickup_location')
        dropoff_location = data.get('dropoff_location')
        travel_medium = data.get('travel_medium')
        start_datetime = data.get('start_datetime')
        asset_capacity = data.get('asset_capacity')

        # validate the input data
        if travel_medium not in ['BUS', 'CAR', 'TRAIN']:
            return JsonResponse({'error': 'Invalid travel medium'}, status=400)
        if not pickup_location or not dropoff_location:
            return JsonResponse({'error': 'Pickup and dropoff locations are required'}, status=400)

        # create the travel route
        route = TravelRoute.objects.create(
            rider=request.user,
            pickup_location=pickup_location,
            dropoff_location=dropoff_location,
            travel_medium=travel_medium,
            start_datetime=start_datetime,
            asset_capacity=asset_capacity
        )

        return redirect('view_travel_routes')
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
