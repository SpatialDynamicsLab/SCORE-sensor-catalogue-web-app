from django.urls import path 
from .views import (
    HomePage,
    DetailView,
    SensorDetailView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_sensor_from_cart,
    )



app_name  = 'catalogue'
urlpatterns =[
    path('', HomePage.as_view(), name='home'),
    # path('checkout/',sensor_list, name='checkout'),
    path('order-summary/',OrderSummaryView.as_view(), name='order-summary'),
    path('sensor/<slug>/',SensorDetailView.as_view(), name='sensor'),

    # path('category/<str:category>/', my_view, name='my_view'),

    # path('filter-by-hazards/', filter_by_hazards,name='filter-by-hazards'),
    # path('filter-by-hazards/', filter_by_hazards,name='filter-by-hazards'),
    # path('filter-by-hazards/', filter_by_hazards,name='filter-by-hazards'),
    path('add-to-cart/<slug>/', add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart,name='remove-from-cart'),
    path('remove-sensor-from-cart/<slug>/', remove_single_sensor_from_cart,name='remove-single-sensor-from-cart')

]