from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from orders.models import OrderItem
from orders.forms import OrderCreateForm
from cart.cart import Cart


@login_required
def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid:
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    sensor=item['sensor'],
                    price=item['price'],
                    quantity=item['quantity'])
            # Clear the cart when done.
            cart.clear()
            request.session['order_id'] = order.id
            send_new_order_email(order)
        return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


def send_new_order_email(order):
    order_items = OrderItem.objects.filter(order=order)
    subject = 'New SCORE sensors selection'
    from_email = 'score@ucd.ie'
    recipient_list = [
        order.user.email,
        'jose.gomezbarron@ucd.ie',
        # 'chiara.cocco@ucd.ie'
    ]
    context = {
        'logo_url': 'https://sensors.score-eu-project.eu/static/images/'
                    'score-sensors-catalogue-big-logo.png',
        'user_name': f"{order.user.first_name} {order.user.last_name}",
        'order_id': order.id,
        'order_items': order_items,
        'total_cost': order.get_order_total()
    }
    html_message = render_to_string('orders/order/order_email.html', context)
    send_mail(
        subject,
        None,
        from_email,
        recipient_list,
        fail_silently=False,
        html_message=html_message
    )
