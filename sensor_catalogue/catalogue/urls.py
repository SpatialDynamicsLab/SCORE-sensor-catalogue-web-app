from django.urls import path 
from . import views

app_name  = 'catalogue'
urlpatterns =[


    # path('', views.home_page, name='home_page'), Main landing page. Do not mess up

    path('', views.home, name='home'),

    path('hazards/', views.hazard_list, name='hazards_list'),

    path('hazards/<slug:slug>', views.hazard_sensor_list, name='hazard_sensor_list'),

    # path('parameters/', views.parameter_list, name='parameter_list'),
    # path('parameters/<slug:slug>', views.parameter_sensor_list, name= 'parameter_sensor_list'),


    # path('install-difficulty/', views.install_difficulty_list, name='install_difficulty_list'),
    # path('install-difficulty/<str:name>', views.install_difficulty_sensor_list, name= 'install_difficulty_sensor_list'),


    path('checkout/',views.CheckoutView.as_view(), name='checkout'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    # path('cart-details/', views.cart_detail, name='cart_detail'),
    # path('sensor/<slug>/',views.SensorDetailView.as_view(), name='sensor'),

    path('sensor/<slug>/',views.detail_view, name='sensor'),

    path('add-to-cart/<slug>/', views.add_to_cart,name='add-to-cart'),
    # path('add_to_cart/<slug>/', views.cart_add,name='cart_add'),
  



    path('remove-from-cart/<slug>/', views.remove_from_cart,name='remove-from-cart'),
    # path('remove_from_cart/<slug>/', views.cart_remove,name='cart_remove'),

    path('remove-sensor-from-cart/<slug>/', views.remove_single_sensor_from_cart,name='remove-single-sensor-from-cart'),
    # path('order/<int:order_id>/pdf/', views.admin_order_pdf, name='order-pdf')
    # path('order/<int:order_id>/', views.admin_order_pdf, name='order-pdf'),
    # path('order/<int:order_id>/', views.admin_order_pdf, name='order-pdf'),
    path('order/<int:order_id>/', views.order_detail, name='order-detail'),

]