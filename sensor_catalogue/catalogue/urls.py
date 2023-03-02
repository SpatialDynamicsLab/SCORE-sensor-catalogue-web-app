from django.urls import path 

from .  import views


app_name  = 'catalogue'
urlpatterns =[
    
    path('', views.hazard_list, name='home'),

    path('<slug:hazard_slug>/', views.hazard_sensor_list, name='hazard_sensor_list'),


    # path('checkout/',checkout, name='checkout'),
    path('checkout/',views.CheckoutView.as_view(), name='checkout'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('sensor/<slug>/',views.SensorDetailView.as_view(), name='sensor'),

    path('add-to-cart/<slug>/', views.add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<slug>/', views.remove_from_cart,name='remove-from-cart'),
    path('remove-sensor-from-cart/<slug>/', views.remove_single_sensor_from_cart,name='remove-single-sensor-from-cart'),
    # path('send-order-email/<int:order_id>/pdf', views.admin_order_pdf, name='admin-order-pdf')
    
]