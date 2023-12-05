import json
from django.shortcuts import render

from navigation.forms import LocationForm
from django.shortcuts import render, redirect
from .models import Location
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import CampusEvent

# Create your views here.


@csrf_exempt
def get_locations(request):
    locations = Location.objects.all()
    data = [{'from_location': location.from_location, 'to_location': location.to_location, 'timestamp': location.timestamp} for location in locations]
    return JsonResponse(data, safe=False)
    
@csrf_exempt
def add_location(request):
    if request.method == 'POST':
        print("API CALL RECICVED")
        data = json.loads(request.body)
        from_location = data.get('from_location')
        to_location = data.get('to_location')

        if from_location and to_location:
            location = Location(from_location=from_location, to_location=to_location)
            location.save()
            return JsonResponse({'message': 'Location added successfully','status':'success'})
        else:
            return JsonResponse({'error': 'Invalid data provided','status':'fail'})
    else:
        return JsonResponse({'error': 'Invalid request method','status':'fail'})
    

@method_decorator(csrf_exempt, name='dispatch')
class CampusEventApiView(View):
    def get(self, request, *args, **kwargs):
        events = CampusEvent.objects.all()
        event_list = [{'id': event.id, 'campus_name': event.campus_name, 'event_name': event.event_name,
                       'event_description': event.event_description, 'event_image': event.event_image.url,
                       'event_timestamp': event.event_timestamp, 'slug': event.slug} for event in events]
        return JsonResponse({'events': event_list}, safe=False)

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
