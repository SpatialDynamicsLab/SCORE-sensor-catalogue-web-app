from django.db import models
from django.db.models import Model,CharField
from django.conf import settings
import uuid
from autoslug import AutoSlugField
import datetime

from django.shortcuts import reverse



PURCHASE_OPERATION_COMPLEXITY_CHOICES = (
    ('VD', 'very difficult'),
    ('DI', 'difficult'),
    ('NE', 'neutral'),
    ('EA', 'easy'),
    ('VE', 'very easy')
)


ASSEMBLY_OPERATION_COMPLEXITY_CHOICES = ( 
    ('VD', 'very difficult'),
    ('DI', 'difficult'),
    ('NE', 'neutral'),
    ('EA', 'easy'),
    ('VE', 'very easy')

)

INSTALLATION_OPERATION_COMPLEXITY_CHOICES = (
    ('VD', 'very difficult'),
    ('DI', 'difficult'),
    ('NE', 'neutral'),
    ('EA', 'easy'),
    ('VE', 'very easy')

)

DATA_ANALYSIS_OPERATION_CHOICES = (
    ('VD', 'very difficult'),
    ('DI', 'difficult'),
    ('NE', 'neutral'),
    ('EA', 'easy'),
    ('VE', 'very easy')

)

CITIZEN_SCIENCE_OPERATION_CHOICES = (
    ('VD', 'very difficult'),
    ('DI', 'difficult'),
    ('NE', 'neutral'),
    ('EA', 'easy'),
    ('VE', 'very easy')

)

INSTALLATION_COST_CHOICES = (
    
    ('H', 'high'),
    ('M', 'medium'),
    ('L', 'low')
)


HAZARD_CHOICES = (
     ('SL', 'Sea level rise'),
     ('CF', 'Coastal flooding'),
     ('LF', 'Land and river flooding'),
     ('CE', 'Coastal Erosion'),
     ('SS', 'Storm Surge'),
     ('DH', 'Droughts and heat waves'),
     ('LS', 'Landslide')
)

YEAR_CHOICES = []
for Y in range(1990, (datetime.datetime.now().year+1)):
     YEAR_CHOICES.append((Y,Y))


class HazardCategory(models.Model):
    hazard_category_name  =  models.CharField(
         max_length=100,
         blank=True,
         null=True)

    class Meta:
         verbose_name = "Hazard Category"
         verbose_name_plural = "Hazard Categories"

    def __str__(self):
        return self.hazard_category_name
    

class HazardSpecific(models.Model):
    hazard_specific_name = models.CharField(
         max_length=65,
         blank=True,
         null=True)

    class Meta:
            verbose_name = "Specific Hazard"
            verbose_name_plural = "Specific Hazard"

    def __str__(self):

        return self.hazard_specific_name


class MonitoredParameter(models.Model):
    monitored_parameter_name = models.CharField(max_length=50)

    class Meta:
         verbose_name = "Monitored Parameter"
         verbose_name_plural = "Monitored Parameters"

    def __str__(self):
        return self.monitored_parameter_name


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Sensor(models.Model):
    id  =  models.UUIDField(
         primary_key=True, 
         default=uuid.uuid4, 
         editable=False)
    id_old = models.CharField(
         max_length=10, 
         verbose_name="OLD ID")
    tested_with_score = models.BooleanField(
         default=True, 
         verbose_name="Tested with SCORE")
    reference_partner = models.CharField(
         max_length=150, 
         verbose_name="Reference partner")
    sensor_name = models.CharField(
         max_length= 250, 
         verbose_name= "Name")
    short_description = models.TextField(
         verbose_name="Short Description")
    full_description = models.TextField(
         verbose_name="Detailed Description")
    monitored_parameter = models.ManyToManyField(
         MonitoredParameter,
         blank=True,
         verbose_name="Monitored Parameter")
    relevant_to_models = models.BooleanField(
         default=True, 
         verbose_name="Relevant to WP3 Models / EWSS")
    hazard = models.CharField(
         choices=HAZARD_CHOICES, 
         max_length=2, 
         verbose_name='Hazard')
    hazard_category= models.ManyToManyField(
         HazardCategory, 
         blank=True,
         verbose_name="Hazard Category")
    hazard_specific= models.ManyToManyField(
         HazardSpecific,
         blank=True,
         verbose_name="Hazard Specific")
    price = models.DecimalField(
         max_digits=10, 
         decimal_places=2,
         verbose_name="Cost(€)")
    sensor_website = models.URLField(
         blank=True, 
         verbose_name="Sensor Web Page")
    project_name = models.CharField(
         max_length=250, 
         verbose_name="Project Name")
    project_year = models.IntegerField(
         choices=YEAR_CHOICES,default=datetime.datetime.now().year,
         verbose_name="Project Year")

    project_website = models.URLField(
         blank=True, 
         verbose_name="Project Website")
    reference_paper = models.URLField(
         blank=True, 
         verbose_name="Reference Paper")
    unit_of_measurement = models.CharField(
         max_length=10, 
         verbose_name="Unit of Measurement")
    accuracy = models.CharField(
         max_length=15, 
         verbose_name="Sensor Accuracy")
    data_refresh_time= models.IntegerField(blank=True,null=True,
         default=5, 
         verbose_name="Data Refresh Duration (Minutes)")
    wifi_connection = models.BooleanField(
         default=True, 
         verbose_name="WiFi Connection")
    mobile_data_connection = models.BooleanField(
         default=True, 
         verbose_name= "4G Connection")
    number_of_components = models.IntegerField(
         null=True, 
         verbose_name="Number of components")
    external_power_supply = models.BooleanField(
         default=False, 
         verbose_name= "External Power Supply")
    minimum_purchase_quantity = models.IntegerField(
         null=True, blank=True, default=1,
         verbose_name="Minimum purchase quantity")
    spatial_density_per_area = models.IntegerField(
         null=True, blank=True,
         verbose_name="Spatial Density / min number per area [km2]")
    spatial_density_distribution = models.TextField(blank=True, null=True, default="Not provided",
         verbose_name="Spatial Density / min number and distribution description")
    # Operation complexities
    purchase_operation = models.CharField(
         choices=PURCHASE_OPERATION_COMPLEXITY_CHOICES, 
         max_length=2, 
         verbose_name="Purchase Operations Complexity")
    assembly_operation = models.CharField(
         choices=ASSEMBLY_OPERATION_COMPLEXITY_CHOICES, 
         max_length=2, 
         verbose_name="Assembly Operations Complexity")
    installation_operation = models.CharField(
         choices=INSTALLATION_OPERATION_COMPLEXITY_CHOICES, 
         max_length=2, 
         verbose_name="Installation Operation Complexity ")
    installation_costs = models.CharField(
         choices=INSTALLATION_COST_CHOICES, 
         max_length=1, 
         verbose_name="Installation Cost")
    data_analysis_operation = models.CharField(
         choices=DATA_ANALYSIS_OPERATION_CHOICES, 
         max_length=2, 
         verbose_name="Data Analysis Operations Complexity")
    citizen_science_operation = models.CharField(
         choices=CITIZEN_SCIENCE_OPERATION_CHOICES, 
         max_length=2, 
         verbose_name="Citizen Science Activities Complexity")
    targeted_user = models.CharField(
         max_length=250, 
         verbose_name="Targeted Users")
    image = models.ImageField(
         upload_to='sensor_pictures/%Y/%m/%d',
         blank=True,
          null=True)
    slug =  AutoSlugField(
         populate_from='sensor_name', 
         unique=True, 
         null=True, 
         default=None)
    

    class Meta:
         verbose_name = "Sensor"
         verbose_name_plural = "Sensors"

    def __str__(self):
        return self.sensor_name
    

    def get_absolute_url(self):
         return reverse("catalogue:sensor", kwargs={
              'slug':self.slug
         })
    

    def get_add_to_cart_url(self):
         return reverse("catalogue:add-to-cart", kwargs = {
              'slug':self.slug
         })

    def get_remove_from_cart_url(self):
         return reverse("catalogue:remove-from-cart", kwargs = {
              'slug':self.slug
         })


class OrderSensor(models.Model):
        user = models.ForeignKey(
             settings.AUTH_USER_MODEL, 
             on_delete=models.CASCADE, blank=True, null=True)
        ordered = models.BooleanField(
             default=False)
        sensor = models.ForeignKey(
             Sensor, 
             on_delete=models.CASCADE)
        quantity = models.IntegerField(default=1)

        def __str__(self):
            return f"{self.quantity} of {self.sensor.sensor_name}"
        
        def get_total_sensor_price(self):
             return self.quantity *self.sensor.price
        
        class Meta:
         verbose_name = "Order Sensor"
         verbose_name_plural = "Order Sensors"

class Order(models.Model):
        user = models.ForeignKey(
             settings.AUTH_USER_MODEL, 
             on_delete=models.CASCADE)
        sensors = models.ManyToManyField(OrderSensor)
        start_date = models.DateTimeField(auto_now_add=True)
        ordered_date = models.DateTimeField()
        ordered = models.BooleanField(default=False)


        def __str__(self):
             return self.user.username
        

        def get_order_total(self):
             total = 0
             for order_sensor in self.sensors.all():
                  total += order_sensor.get_total_sensor_price()
             return total

        class Meta:
            verbose_name = "Order"
            verbose_name_plural = "Orders"



