from django.urls import path
from observations import views


app_name = 'observations'

urlpatterns =[
    path('', views.map_view, name='observations-map'),
    # path('create/',views.checkout, name = 'create_order')
]