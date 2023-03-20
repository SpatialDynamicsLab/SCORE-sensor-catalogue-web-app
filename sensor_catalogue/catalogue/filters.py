import django_filters
from django import forms
from . models import Sensor, InstallationCost


class SensorFilter(django_filters.FilterSet):

    price = django_filters.RangeFilter()
    # installation_operation__name = ['installation_operation__name']
    # installation_operation__name = django_filters.CharFilter(lookup_expr='icontains')
    # monitored_parameter  = django_filters.MultipleChoiceFilter(choices=monitored_parameter.name)
    # hazard = django_filters.TimeFilter()
    # installation_costs = django_filters.MultipleChoiceFilter(choices=InstallationCost.name)


    class Meta:
        model = Sensor
        # fields = ['hazard','monitored_parameter','installation_operation__name' , 'price']
        fields = {
            # 'hazard':['exact'],
            'monitored_parameter':['exact'],
            'installation_operation__name':['exact'],
            # 'price': ['lt', 'gt']
            # 'installation_costs' :['exact']
            }

