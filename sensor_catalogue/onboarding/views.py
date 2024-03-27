import json
import requests
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from .models import Sensor, SensorThing, InstallationStep
from django.http import JsonResponse


@method_decorator(xframe_options_exempt, name='dispatch')
class SensorThingCreateView(View):
    template_name = 'onboarding/sensor_thing_form.html'

    def get(self, request, *args, **kwargs):
        sensor_types_used = Sensor.objects.all().values_list(
            'sensor_type', flat=True).distinct()
        sensor_type_choices = {
            k: v for k, v in Sensor.SENSOR_TYPES if k in sensor_types_used}
        return render(request, self.template_name,
                      {'sensor_type_choices': sensor_type_choices})

    def post(self, request, *args, **kwargs):
        sensor_type = request.POST.get('sensor_type')
        location_json = request.POST.get('location',
                                         '{}')  # Default to empty JSON.
        name = request.POST.get('sensor_name', 'Default Name')
        print(name)

        sensor = Sensor.objects.filter(sensor_type=sensor_type).first()
        if not sensor:
            return JsonResponse({'error': 'Sensor type not found.'}, status=404)

        # Check if location is required and validate it.
        if sensor_type == 'SCK-AQ-DUB':
            try:
                location_coords = json.loads(location_json)
                location = {
                    "geometry": {
                        "type": "Point",
                        "coordinates": [location_coords['lng'],
                                        location_coords['lat']]
                    }
                }
            except (json.JSONDecodeError, KeyError, TypeError):
                return JsonResponse(
                    {'error': 'Invalid or missing location data '
                              'for SCK-AQ sensor type.'},
                    status=400)
        else:
            location = {}  # Set an empty location or an appropriate default.

        properties = [{"name": name}]  # Example properties, modify as needed.

        sensor_thing = SensorThing.objects.create(
            sensor=sensor,
            name=name,
            location=json.dumps(location),
            properties=json.dumps(properties)
        )

        return redirect('onboarding:installation_step',
                        sensor_thing_id=sensor_thing.id)


@xframe_options_exempt
def installation_step_view(request, sensor_thing_id, step_number=1):
    sensor_thing = get_object_or_404(SensorThing, id=sensor_thing_id)
    steps = InstallationStep.objects.filter(
        sensor=sensor_thing.sensor).order_by('step_number')
    current_step = steps.filter(step_number=step_number).first()

    if not current_step:
        return redirect('onboarding:installation_complete')

    next_step_number = step_number + 1 if step_number < steps.count() else None
    prev_step_number = step_number - 1 if step_number > 1 else None
    redirect_url = current_step.redirect_url if not next_step_number else None

    if request.method == 'POST' and current_step.step_type == 'input':
        input_value = request.POST.get('step_input', '').strip()
        properties = json.loads(sensor_thing.properties or '{}')
        print(properties)

        # Ensure properties is a dictionary
        if not isinstance(properties, list):
            properties = []

        key = current_step.title.replace(' ', '_').lower()
        new_property = {key: input_value}
        properties.append(new_property)
        sensor_thing.properties = json.dumps(properties)
        print(sensor_thing.properties)
        sensor_thing.save()

        # Check if there is an input_processing_url to make a GET request
        if current_step.input_processing_url:
            processing_url = f"{current_step.input_processing_url}{input_value}"
            try:
                response = requests.get(processing_url)
                # Handle the response based on your requirements
                # For now, let's log the status code
                print(
                    f"Processing URL responded with status code: "
                    f"{response.status_code}")
            except requests.RequestException as e:
                # Log the exception or handle it as needed
                print(f"Error making GET request to processing URL: {str(e)}")

        messages.success(request, 'Your input has been saved successfully.')

        if next_step_number:
            return redirect(
                reverse('onboarding:installation_step',
                        args=[sensor_thing_id, next_step_number]))
        elif redirect_url:
            return redirect(redirect_url)
        return redirect('onboarding:installation_complete')

    context = {
        'sensor_thing': sensor_thing,
        'current_step': current_step,
        'step_number': step_number,
        'prev_step_number': prev_step_number,
        'next_step_number': next_step_number,
        'total_steps': steps.count(),
        'redirect_url': redirect_url
    }
    return render(request, 'onboarding/installation_step.html', context)


@xframe_options_exempt
def installation_complete_view(request):
    # Define the logic or render a template for the installation completion page
    return render(request, 'onboarding/installation_complete.html')


