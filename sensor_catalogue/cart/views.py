from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.clickjacking import xframe_options_exempt
from django.shortcuts import render, get_object_or_404, redirect
from catalogue.models import Sensor
from cart.forms import CartAddProductForm
from .cart import Cart


@xframe_options_exempt
@require_POST
def cart_add(request, slug):
    cart = Cart(request)
    sensor = get_object_or_404(Sensor, slug=slug)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        clean_data = form.cleaned_data
        cart.add(sensor=sensor,
                 quantity=clean_data['quantity'],
                 quantity_override=clean_data['override'])
    return redirect('cart:cart_detail')


@xframe_options_exempt
@require_GET
def cart_remove(request, slug):
    cart = Cart(request)
    sensor = get_object_or_404(Sensor, slug=slug)
    cart.remove(sensor)
    return redirect('cart:cart_detail')


@xframe_options_exempt
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity':item['quantity'],
            'override': True
            }
        )
        context = {
            'cart':cart,
        }
        return render(request,'cart/cart_detail.html', context)
    else:
        return redirect('catalogue:home')
    