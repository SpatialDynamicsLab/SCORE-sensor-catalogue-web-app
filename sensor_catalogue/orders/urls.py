from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns =[
    path('create/',views.create_order, name = 'create_order')
    # path('create/',views.checkout, name = 'create_order')
]