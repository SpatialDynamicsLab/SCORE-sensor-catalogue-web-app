from django.contrib import admin

from .models import (
    Sensor,
    Order,
    OrderedSensor,
    MonitoredParameter,
    HazardSpecific,
    UserProfile,
    HazardCategory
)


admin.site.register(Order)
admin.site.register(OrderedSensor)
admin.site.register(MonitoredParameter)
admin.site.register(HazardSpecific)
admin.site.register(UserProfile)
admin.site.register(HazardCategory)
admin.site.register(Sensor)