from django.db import models
from catalogue.models import Sensor
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=65)
    second_name = models.CharField(max_length=65)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=110)
    country = CountryField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['-created']),
            ]

    def __str__(self):
        return f"Order {self.id}"

    def get_order_total(self):
        return sum(item.get_cost() for item in self.sensors.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
            Order,
            related_name='sensors',
            on_delete=models.CASCADE
        )
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.quantity * self.price

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
