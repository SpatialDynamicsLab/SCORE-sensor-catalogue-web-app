from django import template
# from catalogue.models import Order
from orders.models import Order

register = template.Library()


@register.filter
def cart_sensor_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(
            user=user, 
            ordered=False)
        if qs.exists():
            return qs[0].sensors.count()
    return 0

import math
@register.filter
def prices_node(value, step):
    if not value: 
        return "P0"
    return f"P{int(math.floor(value / step))}"
