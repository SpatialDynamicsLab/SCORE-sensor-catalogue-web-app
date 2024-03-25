from django.urls import path
from . import views

app_name = 'onboarding'

urlpatterns = [
    # Existing path for creating a new SensorThing
    path('', views.SensorThingCreateView.as_view(),
         name='create-sensor-thing'),

    # Path for installation steps
    path('sensor/<int:sensor_thing_id>/installation-step/',
         views.installation_step_view, name='installation_step'),

    # Path for installation steps with a step number
    path('sensor/<int:sensor_thing_id>/installation-step/<int:step_number>/',
         views.installation_step_view, name='installation_step'),

    # urlpatterns
    path('installation-complete/',
         views.installation_complete_view, name='installation_complete'),

]
