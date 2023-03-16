import django_filters
from . models import Sensor


class SensorFilter(django_filters.FilterSet):
    # hazards = django_filters.filterset(field_name='hazard',loo)

    class Meta:
        model = Sensor
        fields = ['hazard','monitored_parameter','installation_operation']
        # fields = {
        #     'hazard':['exact'],
        #     'monitored_parameter':['exact'],
        #     'installation_operation__name':['exact']}

