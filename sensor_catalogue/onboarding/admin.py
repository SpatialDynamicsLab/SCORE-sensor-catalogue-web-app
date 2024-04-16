from django.contrib import admin
from onboarding.models import Sensor, SensorThing, InstallationStep


# @admin.register(Sensor)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = [
#         f.name for f in Sensor._meta.fields
#     ]


@admin.register(SensorThing)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        f.name for f in SensorThing._meta.fields
    ]


@admin.register(InstallationStep)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        f.name for f in InstallationStep._meta.fields
    ]

