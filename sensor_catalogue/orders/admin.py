from django.contrib import admin
from orders.models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['sensor']

@admin.register(Order)

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'second_name',
        'address',
        'postal_code',
        'city',
        'country',
        'created',
        'updated'
    ]

    list_filter =[
        'created',
        'updated']
    inlines = [OrderItemInline]


