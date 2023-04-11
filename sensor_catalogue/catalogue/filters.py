import django_filters
from django import forms
from . models import Sensor
from django_filters.widgets import RangeWidget


class SensorFilter(django_filters.FilterSet):

    OPERATION_CHOICES = (
    ('VD', 'Very difficult'),
    ('DI', 'Difficult'),
    ('NE', 'Neutral'),
    ('EA', 'Easy'),
    ('VE', 'Very easy'))

   
    price = django_filters.RangeFilter(field_name = 'price',label='Price Range(€)',widget=RangeWidget(attrs={'placeholder':'Enter min/max cost'}))
    deployment_complexity = django_filters.MultipleChoiceFilter(field_name='deployment_operation__name',label="Deployment Complexity", choices=OPERATION_CHOICES)

    class Meta:
        model = Sensor
        fields = ['hazard','monitored_parameter','deployment_complexity']
    
