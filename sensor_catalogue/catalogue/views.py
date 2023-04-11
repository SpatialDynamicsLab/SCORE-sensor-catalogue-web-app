from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



from cart.forms import CartAddProductForm


from .models import Sensor, Hazard, SensorImage

from .filters import SensorFilter




def home(request):
    hazard = request.GET.get('hazard')
    if hazard == None:
        sensors = Sensor.objects.filter(published=True).order_by('price')
        # paginator = Paginator(sensors,9) # 9 sensors per page
        # page = request.GET.get("page")
        # print(request.GET)
        # try:
        #     sensors = paginator.page(page)
        # except PageNotAnInteger:
        #     sensors  = paginator.page(1)
        # except EmptyPage:
        #     sensors  =  paginator.page(paginator.num_pages)
    else:
        sensors = Sensor.objects.filter(published=True).filter(hazard__id=hazard)

    hazards = Hazard.objects.all()
    sensor_filter = SensorFilter(request.GET, queryset=sensors)
    sensors = sensor_filter.qs

    context = {
        'sensors':sensors,
        'hazards':hazards,
        'sensor_filter':sensor_filter
    }

    return render(request, 'index.html', context)


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
        







