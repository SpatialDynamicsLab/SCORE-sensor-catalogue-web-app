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

def order_created(request, order_id):
    user_id = request.user.id
    order =  Order.objects.all(id=order_id)
    subject =f'Order Number .{order.id}'
    message = f'You have successfully placed an order.'\
    f'Ypur order ID is {order.id}'

    mail_sent = send_mail(subject,
                          message,
                          'gabriel.oduori@live.com',
                          [user_id])
    return mail_sent


# def admin_order_pdf(request, order_id):
#     order = get_object_or_404(Order, id=order_id):
#     html= render_to_string('pdf.html',
#                            {'order':order})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition']= f'filename=order_{order_id}.pdf'
#     weasyprint.HTML(string=html).write_pdf(response, 
#                                            stylesheets=[weasyprint.css(
#         settings.STATIC_ROOT + 'css/pdf.css')])
#     return response