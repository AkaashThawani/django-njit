import json
import base64
import mimetypes
import os

from django.conf import settings
from navigation.forms import LocationForm
from .models import Location, SearchLocation
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import CampusEvent, Building, Feedback
from .forms import BuildingForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Login
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.


@csrf_exempt
def get_locations(request):
    locations = SearchLocation.objects.all()
    # print(locations)
    serialize_data = serialize("json", locations)
    serialize_data = json.loads(serialize_data)
    return JsonResponse(serialize_data, safe=False)


@csrf_exempt
def add_location(request):
    if request.method == 'POST':
        print("API CALL RECEIVED")
        data = json.loads(request.body)
        print("data", data)
        # Access data from the payload
        from_location_data = data.get('from_location', {})
        to_location_data = data.get('to_location', {})
        travel_mode = data.get('travel_mode')
        search_by = data.get('search_by') or ''

        from_location_name = from_location_data.get('name')
        from_location_lat = from_location_data.get('lat')
        from_location_lng = from_location_data.get('lng')

        to_location_name = to_location_data.get('name')
        to_location_lat = to_location_data.get('lat')
        to_location_lng = to_location_data.get('lng')

        if (
            from_location_name and from_location_lat and from_location_lng and
            to_location_name and to_location_lat and to_location_lng
        ):
            location = SearchLocation(
                from_location_name=from_location_name,
                from_location_lat=float(from_location_lat),
                from_location_lng=float(from_location_lng),
                to_location_name=to_location_name,
                to_location_lat=float(to_location_lat),
                to_location_lng=float(to_location_lng),
                travel_mode=travel_mode,
                search_by=User(id=search_by)
            )
            print("location", location)
            location.save()
            return JsonResponse({'message': 'Location added successfully', 'status': 'success'})
        else:
            return JsonResponse({'error': 'Invalid data provided', 'status': 'fail'})
    else:
        return JsonResponse({'error': 'Invalid request method', 'status': 'fail'})


@method_decorator(csrf_exempt, name='dispatch')
class CampusEventApiView(View):
    def get(self, request, *args, **kwargs):
        events = CampusEvent.objects.all()
        print(events)
        event_list = [{'campus_name': event.campus_name, 'event_name': event.event_name,
                       'event_org_name': event.organizers_name,'event_location':event.location,
                       'event_type':event.event_type,
                       'event_description': event.event_description, 'event_image': event.event_image.url,
                       'event_start_time': event.start_time,'event_end_time': event.end_time, 'slug': event.slug} for event in events]
        return JsonResponse(event_list, safe=False)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        campus_event = CampusEvent.objects.create(
            campus_name=data['campus_name'],
            event_name=data['event_name'],
            event_description=data['event_description'],
            event_image=data['event_image'],
            event_timestamp=data['event_timestamp'],
            slug=data['slug']
        )
        return JsonResponse({'id': campus_event.id}, status=201)


@csrf_exempt
def get_buildings(request):
    buildings = Building.objects.all()
    data = [
        {
            'build_name': building.build_name,
            'build_img_url': building.build_img.url,  # URL to the image
            'build_description': building.build_description
        }
        for building in buildings
    ]
    return JsonResponse(data, safe=False)


@csrf_exempt
def get_image(request):
    if request.method == 'POST':
        image_filename = json.loads(request.body)['image_filename']
        print("image_file", image_filename)
        image_path = os.path.join(
            settings.BASE_DIR, image_filename)
        print("IMAGE PATH-", image_path)

        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        # Adjust based on your image types (JPEG, PNG, etc.)
        content_type = 'image/jpeg'

        response = HttpResponse(image_data, content_type=content_type)
        response['Content-Disposition'] = f'inline; filename="{image_filename}"'
        return response


@csrf_exempt
def add_building(request):
    if request.method == 'POST':
        print("API CALL RECEIVED")
        data = json.loads(request.body)
        build_name = data.get('build_name')
        build_img = data.get('build_img')
        build_description = data.get('build_description')

        if build_name and build_img and build_description:
            building = Building(
                build_name=build_name, build_img=build_img, build_description=build_description)
            building.save()
            return JsonResponse({'message': 'Building added successfully', 'status': 'success'})
        else:
            return JsonResponse({'error': 'Invalid data provided', 'status': 'fail'})
    else:
        return JsonResponse({'error': 'Invalid request method', 'status': 'fail'})


@csrf_exempt
def get_feedback(request):
    feedback_list = Feedback.objects.all()
    data = [{'user_name': feedback.user_name, 'comment': feedback.comment,
             'timestamp': feedback.timestamp} for feedback in feedback_list]
    return JsonResponse({'data': data, 'status': 'success'}, safe=False,)


@csrf_exempt
def save_feedback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        name = data['name']
        comment = data['comments']
        print(data)
        if email is not None and name is not None and comment is not None:
            newfeedback = Feedback(email=email, name=name, comment=comment)
            newfeedback.save()
            return JsonResponse({'message': 'Feedback saved successfully', 'status': 'success'}, status=200)
        else:
            return JsonResponse({'message': 'Unable to save feedback', 'status': 'fail'}, status=200)
    else:
        return JsonResponse({'message': 'Unable to save feedback', 'status': 'fail'}, status=400)


@csrf_exempt
def get_feedback_by_id(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        feedback_id = data.get('feedback_id')

        if feedback_id:
            feedback = Feedback.objects.get(pk=feedback_id)
            return JsonResponse({'user_name': feedback.user_name, 'comment': feedback.comment, 'timestamp': feedback.timestamp})
        else:
            return JsonResponse({'error': 'Invalid data provided', 'status': 'fail'})
    else:
        return JsonResponse({'error': 'Invalid request method', 'status': 'fail'})


@csrf_exempt
def save_admin_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        feedback_id = data.get('feedback_id')
        admin_comment = data.get('admin_comment')

        if feedback_id and admin_comment:
            feedback = Feedback.objects.get(pk=feedback_id)
            feedback.admin_comment = admin_comment
            feedback.save()
            return JsonResponse({'message': 'Admin comment saved successfully', 'status': 'success'})
        else:
            return JsonResponse({'error': 'Invalid data provided', 'status': 'fail'})
    else:
        return JsonResponse({'error': 'Invalid request method', 'status': 'fail'})


@api_view(['POST'])
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'message': 'User Login success',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user_id': user.id,
                'email': user.email,
                'status': 'success'
            }, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials', 'message': 'Login failed ', 'status': 'fail'}, status=200)


@api_view(['POST'])
@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            # Login.objects.create(user=user, user_type='admin')
            return JsonResponse({'message': 'Admin login successful',
                                 'access_token': str(refresh.access_token),
                                 'refresh_token': str(refresh),
                                 'user_id': user.id,
                                 'email': user.email,
                                 'status': 'success'})
        else:
            return JsonResponse({'message': 'Invalid admin credentials', 'status': 'fail'})


@api_view(['POST'])
@csrf_exempt
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful', 'status': 'success'}, status=200)


@api_view(['POST'])
@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        print("create user", request.data)
        username = request.data.get('email')
        password = request.data.get('password')
        email = request.data.get('email')
        first_name = request.data.get('fName')
        last_name = request.data.get('lName')
        if username is not None and password is not None and email is not None:
            User.objects.create_user(
                username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            return JsonResponse({'message': 'User created successfully', 'status': 'success'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid Payload', 'status': 'fail'}, status=200)


def refresh_token(request):
    return refresh_jwt_token(request)


@api_view(['POST'])
@csrf_exempt
def create_admin(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        User.objects.create_superuser(
            username=username, password=password, email=email, is_staff=True)
        return JsonResponse({'message': 'Admin created successfully', 'status': 'success'})


@api_view(['GET'])
def validate_user_session(request):
    if request.user.is_authenticated:
        return JsonResponse({'message': 'User session is valid', 'status': 'success', 'login': 'true'})
    else:
        return JsonResponse({'message': 'User session is not valid', 'status': 'fail', 'login': 'false'})
