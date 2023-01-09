# Django Lets Ride App
This Django app allows users to share their travel routes and request the transportation of assets.

## Requirements
Run the command `pip install -r requirements.txt` to install all the requirements.

## Running the application
- After cloning this repository run the following commands
> `python manage.py makemigrations`
> `python manage.py makemigrations main`
> `python manage.py migrate --run-syncdb`
- Create a superuser to login as admin
> `python manage.py createsuperuser`
- To start the application run:
> `python manage.py runserver`
- If you want to run the cronjob which checks the expiry status of asset requests you might have to run this in a linux environment
> `python manage.py crontab add`

## Summary of Views.py
- `IndexPageView`: A class-based view that returns an HTML page as the response to a request.

- `view_travel_routes`: A view function that returns an HTML page with a list of travel routes, with 10 routes per page. The page number is specified in the request parameters.

- `view_asset_transportation_requests`: A view function that returns an HTML page with a list of asset transportation requests made by the logged-in user. The requests are filtered and sorted based on the request parameters, and the resulting queryset is paginated with 10 requests per page.

- `view_matching_rides`: A view function that returns an HTML page with a list of travel routes that match certain criteria specified in the request parameters and which are compatible with a given asset transportation request. The matching travel routes are paginated with 10 routes per page.

- `create_asset_transportation_request`: A view function that creates a new asset transportation request based on the form data submitted in the request.

- `apply_to_ride`: A view function that allows the logged-in user to apply to join a travel route with the given ID.

All of these view functions require the user to be logged in.

  
 ## Summary of Models.py
- The `TravelRoute model` represents a travel route shared by a user. It has fields for the rider (a ForeignKey field to the User model, representing the user who is sharing the travel route), pickup location, dropoff location, start datetime, travel medium, asset capacity, and status.
	-  `rider`: a `ForeignKey` field to the `User` model, representing the user who is sharing the travel route
	-   `pickup_location`: a `CharField` for the pickup location of the travel route
	-   `dropoff_location`: a `CharField` for the dropoff location of the travel route
	-   `start_datetime`: a `DateTimeField` for the start datetime of the travel route
	-   `travel_medium`: a `CharField` with choices for the travel medium (bus, car, or train)
	-   `asset_capacity`: a `PositiveIntegerField` for the capacity for assets in the travel route
	-   `status`: a `CharField` with choices for the status of the travel route (applied or not applied)

- The `AssetTransportationRequest model` represents a request for the transportation of an asset. It has fields for the requester (a ForeignKey field to the User model, representing the user who is making the request), pickup location, dropoff location, start datetime, asset type, asset count, sensitivity, status, whom to deliver, rider (a ForeignKey field to the User model, representing the user who is fulfilling the request), and matched routes (a ManyToManyField to the TravelRoute model, representing the travel routes that are compatible with the request).
	-   `requester`: a `ForeignKey` field to the `User` model, representing the user who is making the request
	-   `pickup_location`: a `CharField` for the pickup location of the asset
	-   `dropoff_location`: a `CharField` for the dropoff location of the asset
	-   `start_datetime`: a `DateTimeField` for the start datetime of the request
	-   `asset_type`: a `CharField` with choices for the type of asset (laptop, travel bag, or package)
	-   `asset_count`: a `PositiveIntegerField` for the number of assets in the request
	-   `sensitivity`: a `CharField` with choices for the sensitivity of the asset (highly sensitive, sensitive, or normal)
	-   `status`: a `CharField` with choices for the status of the request (pending, expired, or completed)
	-   `whom_to_deliver`: a `CharField` for the recipient of the asset
	-   `rider`: a `ForeignKey` field to the `User` model, representing the user who is fulfilling the request
	-   `matched_routes`: a `ManyToManyField` to the `TravelRoute` model, representing the travel routes that are compatible with the request
> The `update_expired_records` method of the `AssetTransportationRequest model` updates the status of all expired asset transportation requests to 'Expired'. An asset transportation request is considered expired if its start datetime is in the past.
