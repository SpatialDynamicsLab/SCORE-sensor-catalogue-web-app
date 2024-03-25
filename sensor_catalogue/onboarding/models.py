from django.db import models


class Sensor(models.Model):
    SENSOR_TYPES = [
        ('SCK-AQ', 'Smart Citizen Kit Air Quality'),
        ('WU-PWS', 'BRESSER WIFI ClearView Weather Station with 7-in-1 Sensor'),
    ]

    sensor_type = models.CharField(max_length=10, choices=SENSOR_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SensorThing(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.JSONField()
    properties = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def sensor_directory_path(instance, filename):
    # This function can be used to define a custom upload path
    return 'sensors/{0}/{1}'.format(instance.sensor.id, filename)


class InstallationStep(models.Model):
    STEP_TYPE_CHOICES = (
        ('media', 'Media Presentation'),
        ('input', 'Input Gathering'),
    )

    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    step_number = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    step_type = models.CharField(
        max_length=5, choices=STEP_TYPE_CHOICES, default='media')
    image = models.ImageField(
        upload_to=sensor_directory_path, null=True, blank=True)
    video = models.FileField(
        upload_to=sensor_directory_path, null=True, blank=True)
    input_type = models.CharField(max_length=255, null=True, blank=True)
    input_label = models.CharField(max_length=255, null=True, blank=True)

    # New field for redirect URL or path
    redirect_url = models.URLField(
        max_length=255, null=True, blank=True,
        help_text='URL or path to redirect after the step is completed')
    input_processing_url = models.URLField(
        max_length=255, null=True, blank=True,
        help_text='URL used for processing and input.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sensor', 'step_number']
        unique_together = [['sensor', 'step_number']]

    def __str__(self):
        return (f'{self.sensor.sensor_type} '
                f'Step {self.step_number}: {self.title}')
