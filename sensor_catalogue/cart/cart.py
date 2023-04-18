
from decimal import Decimal
from django.conf import settings
from catalogue.models import Sensor

class Cart:
    def __init__(self, request):
        """
        Initiaize the cart
        """

        self.session  = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID]={}
        self.cart = cart

    def __iter__(self):
        """
        Iterrate over the items in the cart and get the sensors
        from the backend
        """
        sensor_slugs= self.cart.keys()
        # Get the sensor object  and add them to the cart
        sensors = Sensor.objects.filter(slug__in=sensor_slugs)
        cart = self.cart.copy()
        for sensor in sensors:
            cart[str(sensor.slug)]['sensor']=sensor
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price']=item['price'] * item['quantity']
            yield item


    def __len__(self):
        """
        Count all items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, sensor, quantity=1, quantity_override=False):
        """
        Add a product to the cart or update the quantity
        """
        slug = str(sensor.slug)
        if slug not in self.cart:
            self.cart[slug] = {'quantity': 0,
                                        'price':str(sensor.price)}
        if quantity_override:
            self.cart[slug]['quantity'] = quantity
        else:
            self.cart[slug]['quantity'] += quantity
        self.save()

    def save(self):
        # Mark session as modified
        self.session.modified = True

    def remove(self, sensor):
        """
        Remove a sensor from the cart
        """
        slug = str(sensor.slug)
        if slug in self.cart:
            del self.cart[slug]
            self.save()
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    

    def clear(self):
        # Remove cart from session

        del self.session[settings.CART_SESSION_ID]
        self.save()