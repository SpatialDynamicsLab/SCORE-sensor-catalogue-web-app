from django import template
register = template.Library()
import math

@register.filter
def pricesnode(value, step):
    return f"P{int(math.floor(value / step))}"
