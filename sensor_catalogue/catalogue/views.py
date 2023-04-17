from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



from cart.forms import CartAddProductForm


from .models import Sensor, OrderSensor, Order, Hazard, MonitoredParameter, InstallationOperation, SensorImage

from .filters import SensorFilter

import math

def home(request):
    sensors = Sensor.objects.order_by('price')
    hazards = Hazard.objects.all()
    monitored = MonitoredParameter.objects.all()

    # TODO No way for db, maybe it's better to add a 'title' field in InstallationOperation model?
    # titles and loop can be removed in that case, passing only the queryset complexity_qs in complexity
    titles = {
        'VD': 'Very difficult',
        'DI': 'Difficult',
        'NE': 'Neutral',
        'EA': 'Easy',
        'VE': 'Very easy'
    }
    complexity_qs = InstallationOperation.objects.all()
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
    # print(sensor)
    # cart = Cart()
    cart_sensor_form= CartAddProductForm()
    photos = SensorImage.objects.filter(sensor__slug=slug)
    context = {
        'sensor':sensor,
        'photos':photos
    }
        'photos':photos,
        'cart_sensor_form': cart_sensor_form,
        # 'cart':cart,
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
        







