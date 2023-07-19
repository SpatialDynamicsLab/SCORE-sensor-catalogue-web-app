import math
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from cart.forms import CartAddProductForm
from .models import (
    Sensor,
    Hazard,
    MonitoredParameter,
    SensorImage,
    DeploymentOperation,
    SensorFAQ
)


@xframe_options_exempt
def home(request):
    sensors = Sensor.objects.order_by('id')
    hazards = Hazard.objects.all()
    monitored = MonitoredParameter.objects.all()

    # TODO No way for db, maybe it's better to add a 'title' field
    #  in InstallationOperation model?
    # titles and loop can be removed in that case, passing only the
    # queryset complexity_qs in complexity

    """
    This is the current implementation where we have a name field as an 
    OPERATION_CHOICES in the model. 
    These choices are used by a number of fields in the sensor table.
    """
    # titles = {
    #     'VD': 'Very difficult',
    #     'DI': 'Difficult',
    #     'NE': 'Neutral',
    #     'EA': 'Easy',
    #     'VE': 'Very easy'
    # }
    complexity_qs = DeploymentOperation.objects.all()
    complexities = []
    for x in complexity_qs:
        complexity = dict()
        complexity['id'] = x.id
        complexity['title'] = str(x)
        if complexity['title']:
            complexities.append(complexity)
    # END TODO

    sensors_by_price = Sensor.objects.order_by('price')
    if sensors_by_price:
        price_step = sensors_by_price.last().price/20
    else:
        price_step = 100
    min_price = 0 if not sensors_by_price.first() or not \
        sensors_by_price.first().price else sensors_by_price.first().price
    min_price = int(math.floor(min_price / price_step) * price_step)
    max_price = 1000 if not sensors_by_price.last() or \
                        sensors_by_price.last().price > 1000 \
        else sensors_by_price.last().price
    max_price = int(math.ceil(max_price / price_step) * price_step)

    context = {
        'hazards': hazards,
        'monitored': monitored,
        'complexities': complexities,
        'sensors': sensors,
        'min_price': min_price,
        'max_price': max_price,
        'price_step': price_step
    }
    return render(request, 'homepage.html', context)


@xframe_options_exempt
@csrf_exempt
def detail_view(request, slug):
    """
    View for each sensor data in details.
    """
    sensor = get_object_or_404(Sensor, slug=slug)
    cart_sensor_form = CartAddProductForm()
    photos = SensorImage.objects.filter(sensor__slug=slug)
    faqs = SensorFAQ.objects.filter(sensor__slug=slug)
    context = {
        'sensor': sensor,
        'photos': photos,
        'faqs': faqs,
        'cart_sensor_form': cart_sensor_form,
        }
    return render(request, 'sensor.html', context)


@xframe_options_exempt
def hazard_list(request):
    # List of hazards
    hazards = Hazard.objects.all()
    context = {'hazards': hazards}
    return render(request, 'hazard_list.html', context)


@xframe_options_exempt
def hazard_sensor_list(request, slug):
    """
    Pulls a list of hazards and sensors related to them
    """
    if Hazard.objects.filter(slug=slug):
        sensors = Sensor.objects.filter(hazard__slug=slug)
        hazard = Hazard.objects.filter(slug=slug).first()

        context = {'hazard': hazard, 
                   'sensors':sensors}
        return render(request, 'hazard_sensor_list.html', context)
    else:
        return redirect("catalogue:hazards_list")
        







