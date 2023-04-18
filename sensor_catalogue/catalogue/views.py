from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages


from cart.cart import Cart


from cart.forms import CartAddProductForm


from .models import Sensor, Hazard, MonitoredParameter, SensorImage, DeploymentOperation

from .filters import SensorFilter

import math

def home(request):
    sensors = Sensor.objects.order_by('price')
    hazards = Hazard.objects.all()
    monitored = MonitoredParameter.objects.all()

    # TODO No way for db, maybe it's better to add a 'title' field in InstallationOperation model?
    # titles and loop can be removed in that case, passing only the queryset complexity_qs in complexity

    """
    This is the current implementation where we have a name field as an OPERATION_CHOICES in the model. 
    These choices are used by a number of fields in the sensor table.
    """
    titles = {
        'VD': 'Very difficult',
        'DI': 'Difficult',
        'NE': 'Neutral',
        'EA': 'Easy',
        'VE': 'Very easy'
    }
    complexity_qs = DeploymentOperation.objects.all()
    complexities = []
    for x in complexity_qs:
        complexity = dict()
        complexity['id'] = x.id
        complexity['title'] = titles[x.name]
        complexities.append(complexity)
    # END TODO

    price_step = 100
    min_price = 0 if not sensors.first() or not sensors.first().price else sensors.first().price
    min_price = int(math.floor(min_price / price_step) * price_step)
    max_price = 0 if not sensors.last() or not sensors.last().price else sensors.last().price
    max_price = int(math.ceil(max_price / price_step) * price_step)

    context = {
        'hazards':hazards,
        'monitored':monitored,
        'complexities':complexities,
        'sensors':sensors,
        'min_price':min_price,
        'max_price':max_price,
        'price_step':price_step
    }
    return render(request, 'homepage.html', context)


def detail_view(request, slug):
    """
    View for each sensor data in details.
    """
    sensor =  get_object_or_404(Sensor, slug=slug)
    cart_sensor_form= CartAddProductForm()
    photos = SensorImage.objects.filter(sensor__slug=slug)
    context = {
        'sensor':sensor,
        'photos':photos,
        'cart_sensor_form': cart_sensor_form,
        }
    return render(request, 'sensor.html', context)


def hazard_list(request):
    # List of hazards
    hazards = Hazard.objects.all()
    context = {'hazards': hazards}
    return render(request, 'hazard_list.html', context)


def hazard_sensor_list(request, slug):
    """
    Pulls a list of hazards and sensors related to them
    """
    if(Hazard.objects.filter(slug=slug)):
        sensors = Sensor.objects.filter(hazard__slug=slug)
        hazard  = Hazard.objects.filter(slug=slug).first()

        context = {'hazard': hazard, 
                   'sensors':sensors}
        return render(request, 'hazard_sensor_list.html', context)
    else:
        return redirect("catalogue:hazards_list")
        







