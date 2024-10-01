from django.urls import path
from observations import views


app_name = 'observations'

urlpatterns =[
    path('', views.map_view, name='observations-map'),
    path('<int:sensor_id>/', views.map_view, name='map_sensor'),
    path('sta/', views.official_sensors_view, name='official-sensors-map'),
    # path('create/',views.checkout, name = 'create_order')
]