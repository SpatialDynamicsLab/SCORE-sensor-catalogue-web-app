from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from onboarding.models import SensorThing, InstallationStep
from catalogue.models import Sensor


class SensorNameFilter(SimpleListFilter):
    title = _('Sensor by Name')
    parameter_name = 'sensor_name'

    def lookups(self, request, model_admin):
        sensor_list = Sensor.objects.all()
        return [(sensor.id, sensor.sensor_name) for sensor in sensor_list]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(sensor__id=self.value())
        return queryset


@admin.register(SensorThing)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        f.name for f in SensorThing._meta.fields
    ]
    list_filter = (SensorNameFilter,)


@admin.register(InstallationStep)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        f.name for f in InstallationStep._meta.fields
    ]
    list_filter = (SensorNameFilter,)

