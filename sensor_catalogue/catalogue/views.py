from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

from django.utils import timezone

from django.views.generic import View

from .forms import CheckoutForm

from .models import Sensor, OrderSensor, Order, Hazard, MonitoredParameter, InstallationOperation, SensorImage

from .filters import SensorFilter

def is_valid_query(param):
    # Helper function to check if a query is valid
    return param != '' and param is not None


def home_page(request):
    """
    This view serves the main landing page.
    Besides, it also does the fucntion of filtering data, retrning a 
    queryset with either the whole data or as a filter that is 
    then rendered to the template.

    # TO DO.

    Further code refactoring.
    """

    qs = Sensor.objects.order_by('price').all()
    install_ops_complexities = InstallationOperation.objects.all()
    monitored_parameters = MonitoredParameter.objects.order_by('name').all()
    hazards = Hazard.objects.order_by('name').all
    install_operation_difficulties = InstallationOperation.objects.order_by('name').all()
       
    hazard_contains_query = request.GET.get('hazard_contains')
    monitored_parameter_contains_query = request.GET.get('monitored_parameter')
    reference_partner_query = request.GET.get('reference_partner')

    price_min_query = request.GET.get('price_min')
    price_max_query = request.GET.get('price_max')

    project_min_year_query = request.GET.get('project_min_year')
    project_max_year_query = request.GET.get('project_min_year')

    installation_operation_query = request.GET.get('installation_operation')
    

    if is_valid_query(hazard_contains_query) and hazard_contains_query !='Filter by Hazards...':
        qs=qs.filter(hazard__name__icontains=hazard_contains_query)

    elif is_valid_query(reference_partner_query):
        qs=qs.filter(reference_partner__icontains=reference_partner_query)

    if is_valid_query(price_min_query):
        qs = qs.filter(price__gte=price_min_query)

    if is_valid_query(price_max_query):
        qs = qs.filter(price__lt=price_max_query)

    if is_valid_query(project_min_year_query):
        qs = qs.filter(project_year__iexact=project_min_year_query)

    if is_valid_query(project_max_year_query):
        qs = qs.filter(project_year__iexact=project_max_year_query)

    if is_valid_query(installation_operation_query) and installation_operation_query !='Select...':
        qs = qs.filter(installation_operation__name=installation_operation_query)
    
    if is_valid_query(monitored_parameter_contains_query) and monitored_parameter_contains_query !='Select...':
        qs=qs.filter(monitored_parameter__name__icontains=monitored_parameter_contains_query)



    myFilter = SensorFilter(request.GET, queryset=qs)

    qs= myFilter.qs

    context = {
        'queryset':qs,
        'install_ops_complexities':install_ops_complexities,
        'monitored_parameters':monitored_parameters,
        'hazards':hazards,
        'install_operation_difficulties':install_operation_difficulties,
        'myFilter':myFilter
    }
    return render(request, 'index.html', context)


# def multi_select(request):
#     if request.method=="POST":
#         hazard = request.POST.get('hazard_contains')
#         monitored_parameter = request.POST.get('monitored_parameter')
#         installation_operation = request.POST.get('installation_operation')

#         sensor_objects = Sensor.objects.raw('SELECT * FROM SENSORS WHERE hazard="'+hazard_contains_query+'" and monitored_parameter="'+monitored_parameter+'" and installation_operation="'+installation_operation+'"')

#         context = {
#             'sensor_objects': sensor_objects
#         }

#         return 
    
#     else:
#         pass








def detail_view(request, slug):
    """
    View for each sensor data in details.
    """
    sensor =  get_object_or_404(Sensor, slug=slug)
    # print(sensor)
    photos = SensorImage.objects.filter(sensor__slug=slug)
    context = {
        'sensor':sensor,
        'photos':photos
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
        

# def parameter_list(request):
#     # List of monitored parameters
    
#     parameters = MonitoredParameter.objects.all()
#     context = {'parameters': parameters}
#     return render(request, 'parameters.html', context)


# def parameter_sensor_list(request, slug):

#     # Pulls a list of parameters and sensors related to them

#     if(MonitoredParameter.objects.filter(slug=slug)):
#         sensors = Sensor.objects.filter(monitored_parameter__slug=slug)
#         parameter  = MonitoredParameter.objects.filter(slug=slug).first()
#         context = {'sensors':sensors,
#                    'parameter':parameter}
#         return render(request, 'parameters_sensors_list.html', context)
#     else:
#         messages.warning(request, "No such parameter found")
#         return redirect("catalogue:parameter_list")
    

# def install_difficulty_list(request):
#     # Install operation difficluties
    
#     install_operation_difficulties = InstallationOperation.objects.all()
#     print(install_operation_difficulties)
#     context = {'install_operation_difficulties': install_operation_difficulties}
#     return render(request, 'install_operation_difficulty.html', context)


# def install_difficulty_sensor_list(request, name):

#     # Pulls a list of installation difficulties with ralated sensors

#     if(InstallationOperation.objects.filter(name=name)):
#         sensors = Sensor.objects.filter(installation_operation__name=name)
#         parameter  = InstallationOperation.objects.filter(name=name).first()
#         context = {'sensors':sensors,
#                    'parameter':parameter}
#         return render(request, 'Installation_operation__sensors_list.html', context)
#     else:
#         messages.warning(request, "No such parameter found")
#         return redirect("catalogue:install_difficulty_list")



class OrderSummaryView(LoginRequiredMixin,View):
    #Summary of a sensor order
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'order': order
            }
            return render(self.request, 'order_summary.html', context )

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


@login_required
def add_to_cart(request, slug):
    sensor = get_object_or_404(Sensor, slug=slug)
    order_sensor,created = OrderSensor.objects.get_or_create(
        sensor=sensor,
        user=request.user,
        ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        # print(order_qs)
        order = order_qs[0]
        # Now check if the order sensor is in the order
        if order.sensors.filter(sensor__slug=sensor.slug).exists():
            order_sensor.quantity += 1
            order_sensor.save()
            messages.info(request, "This sensor quantity was updated.")
        else:
            order.sensors.add(order_sensor)
            # print("No order created")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.sensors.add(order_sensor)
        messages.info(request, "This sensor was added to your cart.")
    return redirect("catalogue:order-summary")

@login_required
def remove_from_cart(request, slug):
    sensor = get_object_or_404(Sensor, slug=slug)
    order_qs=Order.objects.filter(
        user=request.user,
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if order sensor is in the order
        if order.sensors.filter(sensor__slug=sensor.slug).exists():
            order_sensor = OrderSensor.objects.filter(
                sensor=sensor,
                user = request.user,
                ordered=False
            )[0]
            order.sensors.remove(order_sensor)
            # order_sensor.delete()
            messages.info(request, "This sensor was removed from your cart.")
            return redirect("catalogue:order-summary")
        else:
            messages.info(request, "This sensor was not in your cart.")
            return redirect("catalogue:sensor", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("catalogue:sensor",slug=slug)


@login_required
def remove_single_sensor_from_cart(request, slug):
    sensor = get_object_or_404(Sensor, slug=slug)
    order_qs=Order.objects.filter(
        user=request.user,
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if order sensor is in the order
        if order.sensors.filter(sensor__slug=sensor.slug).exists():
            order_sensor = OrderSensor.objects.filter(
                sensor=sensor,
                user = request.user,
                ordered=False
            )[0]

            if order_sensor.quantity >1:
                order_sensor.quantity -= 1
                order_sensor.save()
            else:
                order.sensors.remove(order_sensor)
            messages.info(request, "This sensor quantity was updated.")
            return redirect("catalogue:order-summary")
        else:
            messages.info(request, "This sensor was not in your cart.")
            return redirect("catalogue:order-summary", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("catalogue:order-summary",slug=slug)

def checkout(request):
    return render(request,'checkout.html')


class CheckoutView(View):

# Orders checkout view 
    def get(self,*args, **kwargs):
        # add the form here
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'form':form,
            'order':order
        }
        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):

        form = CheckoutForm(self.request.POST or None)

        try:
            order = Order.objects.get(user = self.request.user, ordered=False)
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')
                # save_info = form.cleaned_data.get('save_info')
                order.save()
                return redirect('catalogue:checkout')
            messages.warning(self.request,"Email not sent. We are working to fix this functionality.")
            return redirect('catalogue:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("catalogue:order-summary")

@login_required
def admin_order_pdf(request, order_id):
    # Create a pdf page from the order and send to  logged user as an email attatchment
    order = get_object_or_404(Order, id=order_id)
    html= render_to_string('pdf.html',
                           {'order':order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition']= f'filename=order_{order_id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.css(
        settings.STATIC_ROOT + 'css/pdf.css')])
    return redirect('catalogue:home')