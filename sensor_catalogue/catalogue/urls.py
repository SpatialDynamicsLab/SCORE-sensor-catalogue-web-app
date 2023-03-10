from django.urls import path 

from .  import views


app_name  = 'catalogue'
urlpatterns =[


    path('', views.SensorFilterView, name='home_page'),
    path('hazards/', views.hazard_list, name='home'),

    path('hazards/<slug:slug>', views.hazard_sensor_list, name='hazard_sensor_list'),

    path('parameters/', views.parameter_list, name='parameter_list'),
    path('parameters/<slug:slug>', views.parameter_sensor_list, name= 'parameter_sensor_list'),


    path('checkout/',views.CheckoutView.as_view(), name='checkout'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    # path('sensor/<slug>/',views.SensorDetailView.as_view(), name='sensor'),

    path('sensor/<slug>/',views.detail_view, name='sensor'),

    path('add-to-cart/<slug>/', views.add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<slug>/', views.remove_from_cart,name='remove-from-cart'),
    path('remove-sensor-from-cart/<slug>/', views.remove_single_sensor_from_cart,name='remove-single-sensor-from-cart'),
    # path('send-order-email/<int:order_id>/pdf', views.admin_order_pdf, name='admin-order-pdf')
    
]