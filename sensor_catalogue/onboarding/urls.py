from django.urls import path
from . import views
from .views import create_installation_step, get_available_step_numbers
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

    path('data/', views.onboarded_sensor_data_view, name='onboarded_sensor_data'),

    path('edit/', create_installation_step, name='new_installation_step'),
    path('update-step-order/', views.update_step_order, name='update_step_order'),
    path('update-step/<int:step_id>/', views.update_step, name='update_step'),
# New path for fetching available step numbers
    path('api/available-step-numbers/<int:sensor_id>/', get_available_step_numbers, name='available_step_numbers'),
]
