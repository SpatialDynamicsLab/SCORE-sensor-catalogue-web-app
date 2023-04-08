# from io import BytesIO
# from celery import Task
# from django.template import render_to_string
# from django.core.mail import EmailMessage
# from django.conf import settings
# from .models import Order


from django.contrib.auth.decorators import login_required
from celery import Task
from django.core.mail import send_mail
from .models import Order


@login_required
@Task

def order_created(order_id):
    """
    This tasks role is to send out an email when notofcation when an order is 
    successfully created
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' \
    f'You have successfully placed an order.' \
    f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [order.email])
    
    return mail_sent


