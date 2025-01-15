import json
import requests
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from .models import Sensor, SensorThing, InstallationStep
from django.http import JsonResponse
from .forms import InstallationStepForm
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import Max
from django.contrib.auth.decorators import login_required

@method_decorator(xframe_options_exempt, name='dispatch')
class SensorThingCreateView(View):
    template_name = 'onboarding/sensor_thing_form.html'

    def get(self, request, *args, **kwargs):
        # Fetch sensors with their IDs and names
        sensor_ids_names = Sensor.objects.filter().values_list(
            'id', 'sensor_name').distinct()

        # Prepare list of IDs for filtering InstallationSteps
        sensor_ids = [sensor_id for sensor_id, name in sensor_ids_names]

        # Find IDs that have at least one InstallationStep
        valid_sensor_ids = InstallationStep.objects.filter(
            sensor_id__in=sensor_ids
        ).values_list('sensor_id', flat=True).distinct()

        # Create dictionary for dropdown, only include valid sensors
        valid_sensors = {sensor_id: name for sensor_id, name in sensor_ids_names
                         if sensor_id in valid_sensor_ids}

        context = {
            'select_sensor_type': _("Select the Type of Sensor:"),
            'valid_sensors': valid_sensors
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        sensor_type = request.POST.get('sensor_type')
        location_json = request.POST.get(
            'location', '{}')

        sensor = Sensor.objects.filter(id=sensor_type).first()
        if not sensor:
            return JsonResponse(
                {'error': 'Sensor type not found.'}, status=404)

        # Check if location is required and validate it.
        if sensor.id != 18:
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
                    {'error': 'Invalid or missing location data.'},
                    status=400)
        else:
            location = {}  # Set an empty location or an appropriate default.

        # properties = [{"name": name}]  # Example properties, modify as needed.

        sensor_thing = SensorThing.objects.create(
            sensor=sensor,
            location=json.dumps(location),
        )

        return redirect('onboarding:installation_step',
                        sensor_thing_id=sensor_thing.id)


@xframe_options_exempt
def installation_step_view(request, sensor_thing_id, step_number=1):
    sensor_thing = get_object_or_404(SensorThing, id=sensor_thing_id)
    if sensor_thing.sensor.id == 61:
        sck_sensor = True
    else:
        sck_sensor = False
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

        # Ensure properties is a dictionary
        if not isinstance(properties, list):
            properties = []

        key = current_step.title.replace(' ', '_').lower()
        new_property = {key: input_value}
        properties.append(new_property)
        sensor_thing.properties = json.dumps(properties)

        contains_name = 'name' in current_step.title.lower()
        contains_sensor = 'sensor' in current_step.title.lower()
        if (contains_sensor and contains_name
                or current_step.input_type == 'sensor_name'):
            sensor_thing.name = input_value
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
        'redirect_url': redirect_url,
        'sck_sensor': sck_sensor,
    }
    return render(request, 'onboarding/installation_step.html', context)


@xframe_options_exempt
def installation_complete_view(request):
    # Define the logic or render a template for the installation completion page
    return render(request, 'onboarding/installation_complete.html')


def onboarded_sensor_data_view(request):
    # Get all SensorThing objects
    sensor_things = SensorThing.objects.all().order_by('-created_at')
    context = {
        'sensor_things': sensor_things,
    }

    return render(request,
                  'onboarding/onboarded_sensor_data.html',
                  context)
@login_required
def create_installation_step(request):
    sensors = Sensor.objects.filter(published=True).order_by('id')
    steps = InstallationStep.objects.all()  # Get all steps

    if request.method == 'POST':
        form = InstallationStepForm(request.POST, request.FILES)
      
        if form.is_valid():
            form.save()
           # Redirect to a success page or another relevant view
    else:
        form = InstallationStepForm()

    return render(request, 'onboarding/installation_step_form.html', {
        'form': form,
        'sensors': sensors,
        'steps': steps,
    })


@csrf_exempt
def update_step_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sensor_id = data.get('sensor_id')
            ordered_step_ids = data.get('ordered_step_ids', [])

            if not sensor_id or not ordered_step_ids:
                return JsonResponse({'success': False, 'error': 'Missing sensor ID or step IDs'}, status=400)
            
            steps = InstallationStep.objects.filter(sensor_id=sensor_id, id__in=ordered_step_ids)
             # Ensure all ordered_step_ids belong to the specified sensor
            if steps.count() != len(ordered_step_ids):
                return JsonResponse({
                    'success': False,
                    'error': 'Some steps do not belong to the specified sensor.'
                }, status=400)

            # Update step order atomically
            with transaction.atomic():
                # Temporarily assign high step numbers to avoid conflicts
                for step in steps:
                    step.step_number = 1000 + step.id  # Unique temporary value
                    step.save()

                # Assign new step numbers based on the provided order
                for index, step_id in enumerate(ordered_step_ids, start=1):
                    step = InstallationStep.objects.get(id=step_id)
                    step.step_number = index
                    step.save()




            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
           

@csrf_exempt
def update_step(request, step_id):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            step = InstallationStep.objects.get(id=step_id)

            # List of valid fields for InstallationStep model
            valid_fields = [
                'step_number', 'title', 'description',
                'image', 'video', 'input_type', 'input_label',
                'redirect_url', 'input_processing_url'
            ]

            # Only update fields that are in the valid fields list
            for field, value in data.items():
                if field in valid_fields:
                    setattr(step, field, value)

            step.save()  # Save to database
            return JsonResponse({"success": True})
        except InstallationStep.DoesNotExist:
            return JsonResponse({"success": False, "error": "Step not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})


def get_available_step_numbers(request, sensor_id):
    if request.method == "GET":
        # Get all assigned step numbers for the sensor
        assigned_step_numbers = InstallationStep.objects.filter(
            sensor_id=sensor_id
        ).values_list('step_number', flat=True)
        print(assigned_step_numbers)
        # Define the range of step numbers (1-100, for example)
        max_steps = 100
        available_step_numbers = [
            i for i in range(1, max_steps + 1) if i not in assigned_step_numbers
        ]

        return JsonResponse({
            'available_step_numbers': available_step_numbers,
             'assigned_step_numbers': list(assigned_step_numbers),  # Convert QuerySet to a list
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)