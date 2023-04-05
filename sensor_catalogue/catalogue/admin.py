from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from catalogue.models import (
    Sensor,
    Order,
    OrderSensor,
    MonitoredParameter,
    HazardSpecific,
    UserProfile,
    HazardCategory,
    SensorImage,
    Hazard,
    PurchaseOperation,
    AssemblyOperation,
    DeploymentCost,
    DeploymentOperation,
    DataAnalysisOperation,
    CitizenScienceOperation
)


admin.site.register(Order)
admin.site.register(OrderSensor)
admin.site.register(MonitoredParameter)
admin.site.register(HazardSpecific)
admin.site.register(UserProfile)
admin.site.register(HazardCategory)
admin.site.register(PurchaseOperation)
admin.site.register(Hazard)
admin.site.register(AssemblyOperation)
admin.site.register(DeploymentOperation)
admin.site.register(DataAnalysisOperation)
admin.site.register(DeploymentCost)
admin.site.register(CitizenScienceOperation)



class SensorImageInline(admin.TabularInline):
    model = SensorImage
    readonly_fields = (
        'id',

    )

    extra = 1

def order_pdf(obj):
    url = reverse('catalogue:order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf.short_description = 'Invoice'


@admin.register(Sensor)
class SenorImageAdmin(admin.ModelAdmin):
    inlines = [SensorImageInline]

# @admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display =['id', 'email',order_pdf]

