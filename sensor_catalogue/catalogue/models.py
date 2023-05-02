from django.db import models
from django.db.models import Model, CharField
from django.conf import settings
from autoslug import AutoSlugField
import datetime

from django.shortcuts import reverse


OPERATION_CHOICES = (
    ('VD', 'Very difficult'),
    ('DI', 'Difficult'),
    ('NE', 'Neutral'),
    ('EA', 'Easy'),
    ('VE', 'Very easy'))

DEPLOYMENT_COST_CHOICES = (
    ('H', 'High'),
    ('M', 'Medium'),
    ('L', 'Low'))


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


class Hazard(models.Model):
         name = models.CharField(max_length=200, blank=True)
         description = models.TextField(blank=True,default='Not provided')
         image = models.ImageField(upload_to = 'hazards_image/%Y/%m/%d',blank=True,null=True)
         slug = AutoSlugField(
              populate_from='name', 
              max_length=200,
              unique=True, 
              null=True,
               default=None )
         
         class Meta:
              ordering = ['name']
              indexes = [
                   models.Index(fields=['name']),
              ]
              verbose_name = 'Hazard'
              verbose_name_plural = 'Hazards'

         def __str__(self):
              return self.name
         
         def get_absolute_url(self):
              return reverse('catalogue:sensor_list_by_hazard',
                             args=[self.slug])
         

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
    name = models.CharField(max_length=100)
    slug = AutoSlugField(
              populate_from='name', 
              max_length=200,
              unique=True, 
              null=True )

    class Meta:
         verbose_name = "Monitored Parameter"
         verbose_name_plural = "Monitored Parameters"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
         return reverse("catalogue:measured_parameter_list", kwargs={
              'slug':self.slug
         })
    

class CommonInfo(models.Model):
     name = models.CharField(
         choices=OPERATION_CHOICES, 
         max_length=2,
         blank=True,
         default=None)
     image = models.ImageField(upload_to='difficulty/%Y/%m/%d',blank=True,null=True)
     slug = AutoSlugField(
              populate_from='name', 
              max_length=200,
              unique=True, 
              null=True )
     
     class Meta:
        abstract = True


class PurchaseOperation(CommonInfo):
     class Meta:
         verbose_name = "Assembly Operation"
         verbose_name_plural = "Assembly Operations"

     def __str__(self):
        return self.get_name_display()


class AssemblyOperation(CommonInfo):
     
     class Meta:
         verbose_name = "Assembly Operation"
         verbose_name_plural = "Assembly Operations"

     def __str__(self):
        return self.get_name_display()
    
     
class DeploymentOperation(CommonInfo):
    
     class Meta:
         verbose_name = "Deployment Operation Complexity"
         verbose_name_plural = "Deployment Operation Complexities"

     def __str__(self):
        return self.get_name_display()


class PurchaseOperation(CommonInfo):
     class Meta:
         verbose_name = "Purchase Operation Complexity"
         verbose_name_plural = "Purchase Operation Complexities"

     def __str__(self):
        return self.get_name_display()
     

class DeploymentCost(models.Model):
     name = models.CharField(
     choices=DEPLOYMENT_COST_CHOICES,
     max_length=1, blank=True)
     image = models.ImageField(upload_to='deployment_cost/%Y/%m/%d',blank=True,null=True)


     class Meta:
          verbose_name = "Deployment Cost"
          verbose_name_plural = "Deployment Costs"


     def __str__(self):
        return self.get_name_display()


class DataAnalysisOperation(CommonInfo):    
     class Meta:
         verbose_name = "Data Analysis Operation Complexity"
         verbose_name_plural = "Data Analysis Operation Complexities"

     def __str__(self):
        return self.get_name_display()
     
    
class CitizenScienceOperation(CommonInfo):
     
     class Meta:
         verbose_name = "Citizen Science Operation Complexity"
         verbose_name_plural = "Citizen Science Operation Complexities"

     def __str__(self):
        return self.get_name_display()
     

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Sensor(models.Model):
    id_old = models.CharField(
         blank=True,
         max_length=20, 
         verbose_name="Sensor Old ID")
    tested_with_score = models.BooleanField(
         default=True, 
         verbose_name="Tested with SCORE")
    reference_partner = models.CharField(
         blank=True,
         max_length=150, 
         default=None, 
         verbose_name="Reference partner")
    sensor_name = models.CharField(
         max_length= 250, 
         verbose_name= "Name")
    short_description = models.TextField(
         blank=True,
         verbose_name="Short Description")
    full_description = models.TextField(
         blank=True,
         verbose_name="Detailed Description")
    monitored_parameter = models.ManyToManyField(
         MonitoredParameter,
         blank=True,
         verbose_name="Monitored Parameter")
    relevant_to_models = models.BooleanField(
         default=True, 
         verbose_name="Relevant to WP3 Models / EWSS")

    hazard = models.ManyToManyField(Hazard, blank=True, verbose_name="Hazard")

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
         blank=True,
         verbose_name="Cost(€)")
    sensor_website = models.URLField(
         blank=True, 
         verbose_name="Sensor Web Page")
    project_name = models.CharField(
         max_length=250, 
         default=None, 
         verbose_name="Project Name",
         blank=True)
    project_year = models.IntegerField(
         choices=YEAR_CHOICES,default=datetime.datetime.now().year,
         verbose_name="Project Year",
         blank=True,
         null=True)

    project_website = models.URLField(
         blank=True, 
         null=True,
         verbose_name="Project Website")
    reference_paper = models.URLField(
         blank=True, 
         verbose_name="Reference Paper")
    
    accuracy = models.CharField(
         blank=True,null=True,
         max_length=250, 
         verbose_name="Accuracy (error of the measurements)")
    
    unit_of_measurement = models.CharField(
         blank=True,null=True,
         max_length=250, 
         verbose_name="Unit of Measurement")

    data_refresh_time= models.PositiveIntegerField(blank=True,null=True,
         default=5, 
         verbose_name="Data Refresh Duration (Minutes)")
    wifi_connection = models.BooleanField(
         default=True, 
         verbose_name="Wi-Fi Connection")
    mobile_data_connection = models.BooleanField(
         default=True, 
         verbose_name= "4G Connection")
    number_of_components = models.IntegerField(
         null=True, 
         verbose_name="Number of components",
         blank=True)
    external_power_supply = models.BooleanField(
         default=False, 
         verbose_name= "External Power Supply")
    minimum_purchase_quantity = models.PositiveIntegerField(
         null=True, blank=True, default=1,
         verbose_name="Minimum purchase quantity")
    spatial_density_per_area = models.PositiveIntegerField(
         null=True, blank=True,
         verbose_name="Spatial Density / min number per area [km2]")
    spatial_density_distribution = models.TextField(blank=True, null=True, default="Not provided",
         verbose_name="Spatial Density / min number and distribution description")

    purchase_operation = models.ForeignKey(
         PurchaseOperation, 
         on_delete=models.CASCADE,
         blank=True,
         default=None,null=True,
         verbose_name="Purchase Operation")
    
    assembly_operation = models.ForeignKey(
         AssemblyOperation,
         on_delete=models.CASCADE,
         default=None,
         max_length=2,
         blank=True,
         null=True,
         verbose_name="Assembly Operations Complexity")

    assembly_operation_public_involvement = models.TextField(
         blank=True,
         null=True,
         verbose_name="Public Involvement & Assembly Operations")
    
    deployment_operation = models.ForeignKey(
         DeploymentOperation,
         on_delete=models.CASCADE,
         max_length=2, blank=True,null=True,
         default=None, 
         verbose_name="Deployment operation Complexity")
    
    deployment_operation_public_involvement = models.TextField(
         blank=True,
         null=True,
         verbose_name="Public Involvement & Deployment Operations")

#     deployment_costs = models.CharField(
#         choices=DEPLOYMENT_COST_CHOICES,
#         max_length=1, blank=True,
#         default=None, null=True,
#         verbose_name="Deployment Cost")
    
    deployment_costs = models.ForeignKey(
        DeploymentCost,
        on_delete=models.CASCADE,
        max_length=1, blank=True,
        default=None, null=True,
        verbose_name="Deployment Cost")
    

    
    data_analysis_operation = models.ForeignKey(
         DataAnalysisOperation,
         on_delete=models.CASCADE,
         default=None,      
         max_length=2, blank=True,null=True,
         verbose_name="Data Analysis Operations Complexity")
    
    data_analysis_public_involvement = models.TextField(
         blank=True,
         null=True,
         verbose_name="Public Involvement & Data Analysis Operations")
    
    citizen_science_operation = models.ForeignKey(
         CitizenScienceOperation,
         on_delete=models.CASCADE,
         default=None,   
         max_length=2, 
         blank=True, null=True,
         verbose_name="Citizen Science Activities Complexity")
    
    targeted_user = models.CharField(
         max_length=250, blank=True,
         verbose_name="Targeted Users")
    image = models.ImageField(upload_to='sensor_images/%Y/%m/%d',blank=True,null=True)
    slug =  AutoSlugField(
         populate_from='sensor_name', 
         unique=True, 
         null=True, 
         default=None)
    published = models.BooleanField(
         default=False,
         null=False
    )
    
    class Meta:
         verbose_name = "Sensor"
         verbose_name_plural = "Sensors"

    def __str__(self):
        return self.sensor_name
    

    def name_summary(self):
         if len(self.sensor_name) <26:
              return self.sensor_name
         else:
              return self.sensor_name[:26]+"..."
    

    def short_summary(self):
         if len(self.short_description) < 180:
              return self.short_description
         else:
              return self.short_description[:180]+"..."
    

    def get_absolute_url(self):
         return reverse("catalogue:sensor", kwargs={
              'slug':self.slug
         })
    
    def hazards_filters(self):
         return self.hazard.all().values_list("id", flat=True)
    
    def monitored_filters(self):
         return self.monitored_parameter.all().values_list("id", flat=True)
    
    def complexity_filter(self):
          #  Installation operation was renamed to deployment operation.
          #  The next line is therefore needs to be updated

        # if self.installation_operation:
        if self.deployment_operation:
            return self.deployment_operation.id
        return
    
#     def get_minimum_quantity(self):
#         return self.minimum_purchase_quantity

class SensorImage(models.Model):
    sensor = models.ForeignKey(Sensor, default=None, on_delete=models.CASCADE)
    images = models.ImageField(upload_to = 'sensor_images/%Y/%m/%d',blank=True)
 
    def __str__(self):
        return self.sensor.sensor_name
    

    class Meta:
         verbose_name = "Sensor Image"
         verbose_name_plural = "Sensor Images"
