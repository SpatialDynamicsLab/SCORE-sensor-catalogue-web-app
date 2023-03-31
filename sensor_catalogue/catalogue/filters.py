import django_filters
from django import forms
from . models import Sensor
from django_filters.widgets import RangeWidget


class SensorFilter(django_filters.FilterSet):

    # def __init__(self,*args,**kwargs):
    # price_values = [s.price for s in Sensor.objects.all()] 
    # min_price = min(price_values)
    # max_price = max(price_values)
  


    OPERATION_CHOICES = (
    ('VD', 'Very difficult'),
    ('DI', 'Difficult'),
    ('NE', 'Neutral'),
    ('EA', 'Easy'),
    ('VE', 'Very easy'))

   

    # price = django_filters.RangeFilter(label="Enter price range(€):")
    price = django_filters.RangeFilter(widget=RangeWidget(attrs={'placeholder':'Enter min/max cost'}))
    # enter_min_max_price = django_filters.RangeFilter(field_name='price',widget=RangeWidget())

    installation_complexity = django_filters.ChoiceFilter(field_name='deployment_operation__name',label="Installation Complexity", choices=OPERATION_CHOICES)

    class Meta:
        model = Sensor
        fields = ['hazard','monitored_parameter','installation_complexity']
    
