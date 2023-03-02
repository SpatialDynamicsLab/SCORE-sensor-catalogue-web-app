from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

from django.utils import timezone

from django.views.generic import ListView, DetailView, View

from .forms import CheckoutForm

from .models import Sensor, OrderSensor, Order, Hazard


class LandingPage(ListView):
    model = Hazard
    # template_name = "home.html"
    template_name = "index2.html"


def hazard_list(request):
    hazards = Hazard.objects.all()
    context = {'hazards': hazards}
    return render(request, 'hazard_list.html', context)


def hazard_sensor_list(request, hazard_slug):
    hazard = get_object_or_404(Hazard, slug=hazard_slug)
    print(hazard)
    context = {'hazard': hazard}
    # return render(request, 'hazard_sensor_list.html', context)
    # return render(request, 'home.html', context)
    return render(request, 'index.html', context)





class HomePage(ListView):
    model = Sensor
    paginate_by = 10
    template_name = "index.html"



class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context )

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")



class SensorDetailView(DetailView):
    model = Sensor
    template_name = "sensor.html"


@login_required
def add_to_cart(request, slug):
    sensor = get_object_or_404(Sensor, slug=slug)
    order_sensor,created = OrderSensor.objects.get_or_create(
        sensor=sensor,
        user=request.user,
        ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # Now check if the order sensor is in the order
        if order.sensors.filter(sensor__slug=sensor.slug).exists():
            order_sensor.quantity += 1
            order_sensor.save()
            messages.info(request, "This sensor quantity was updated.")
        else:
            order.sensors.add(order_sensor)
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
            message.error(self.request, "You do not have an active order")
            return redirect("catalogue:order-summary")


@login_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html= render_to_string('pdf.html',
                           {'order':order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition']= f'filename=order_{order_id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.css(
        settings.STATIC_ROOT + 'css/pdf.css')])
    return redirect('catalogue:home')