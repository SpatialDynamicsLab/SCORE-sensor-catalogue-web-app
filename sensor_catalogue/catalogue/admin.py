from django.contrib import admin

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
    InstallationOperation,
    InstallationCost,
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
admin.site.register(InstallationOperation)
admin.site.register(DataAnalysisOperation)
admin.site.register(InstallationCost)
admin.site.register(CitizenScienceOperation)



class SensorImageInline(admin.TabularInline):
    model = SensorImage
    readonly_fields = (
        'id',

    )

    extra = 1


@admin.register(Sensor)
class SenorImageAdmin(admin.ModelAdmin):
    inlines = [SensorImageInline]

